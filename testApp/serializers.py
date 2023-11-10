from rest_framework import serializers
from django.db import transaction, IntegrityError
from .models import Category, Product, Customer, Order, OrderItem
from django.db.models import F


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

    def validate(self, data):
        products = data.get('products', [])

        for item in products:
            stock = item['product'].stock
            quantity = item['quantity']

            if self.instance:
                # For updating an existing order
                if stock == 0:
                    raise serializers.ValidationError("No stock available.")
                if quantity > stock:
                    raise serializers.ValidationError("The quantity exceeds the available stock.")
            else:
                # For creating a new order
                if quantity <= 0:
                    raise serializers.ValidationError("Quantity must be a positive integer.")
                if quantity > stock:
                    raise serializers.ValidationError("The quantity exceeds the available stock.")

        return data

    def create(self, validated_data):
        products_data = validated_data.pop('products', [])
        order = Order.objects.create(**validated_data)
        total_price = 0

        with transaction.atomic():
            for product_data in products_data:
                product = product_data['product']
                quantity = product_data['quantity']

                OrderItem.objects.create(order=order, product=product, quantity=quantity)
                product.stock = F('stock') - quantity
                product.save()
                total_price += product.price * quantity

        order.total_price = total_price
        return order

    def update(self, instance, validated_data):
        instance.customer = validated_data.get('customer', instance.customer)
        instance.total_price = validated_data.get('total_price', instance.total_price)
        instance.save()

        products_data = validated_data.get('products', [])
        products_data_list = [item['product'] for item in products_data]
        total_price = 0

        with transaction.atomic():
            for product_data in products_data:
                product_id = product_data['product'].id
                quantity = product_data['quantity']

                order_item, created = OrderItem.objects.get_or_create(
                    order=instance, product_id=product_id, defaults={'quantity': quantity}
                )

                product_data['product'].stock = F('stock') - quantity
                product_data['product'].save()
                total_price += product_data['product'].price * quantity
                order_item.quantity = quantity
                order_item.save()

        instance.total_price = total_price
        OrderItem.objects.filter(order=instance).exclude(product__in=products_data_list).delete()

        return instance

    def destroy(self, instance):
        # Loop through order items and update product stock
        for order_item in instance.products.all():
            order_item.product.stock += order_item.quantity
            order_item.product.save()

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
