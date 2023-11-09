from rest_framework import serializers

from .models import Category, Product, Customer, Order, OrderItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'stock']

    def get_stock(self, obj):
        return obj.product.stock


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        # Extract and remove the nested 'products' data from the validated data
        products_data = validated_data.pop('products', [])

        # Create the order instance without the 'products' field
        order = Order.objects.create(**validated_data)

        total_price = 0

        # Now, create the OrderItem instances and associate them with the order
        for product_data in products_data:
            product = product_data['product']
            quantity = product_data['quantity']

            # Create OrderItem instance and associate it with the order
            OrderItem.objects.create(order=order, product=product, quantity=quantity)
            total_price += product.price * quantity

        order.total_price = total_price
        return order

    def update(self, instance, validated_data):
        # Update fields of the order instance
        instance.customer = validated_data.get('customer', instance.customer)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        # Update or create OrderItem instances
        products_data = validated_data.get('products', [])
        products_data_list = [
            item['product'] for item in products_data
        ]

        total_price = 0
        for product_data in products_data:
            product_id = product_data['product'].id
            quantity = product_data['quantity']

            # Try to get existing OrderItem or create a new one
            order_item, created = OrderItem.objects.get_or_create(order=instance, product_id=product_id,
                                                                  defaults={'quantity': quantity})

            if not created:
                # If the OrderItem already exists, update the quantity
                order_item.quantity = quantity
                total_price += product_data['product'].price * quantity
                order_item.save()

        instance.total_price = total_price
        OrderItem.objects.filter(order=instance).exclude(product__in=products_data_list).delete()

        return instance

    def destroy(self, instance):
        # Delete the order and associated OrderItem instances
        instance.products.all().delete()
        instance.delete()

    def to_representation(self, instance):
        # Use this method for GET requests to customize the serialized representation
        representation = super().to_representation(instance)

        # Retrieve and serialize the related OrderItem instances
        order_items = OrderItem.objects.filter(order=instance)
        representation['products'] = OrderItemSerializer(order_items, many=True).data

        return representation
