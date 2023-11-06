from django.db.models import Model
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


def get_instance_from_dict(data_dict):
    instance_dict = {}
    for key, value in data_dict.items():
        if isinstance(value, Model):
            instance_dict[key] = value
    return instance_dict


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    products = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        order = Order.objects.create(**validated_data)

        for product_data in products_data:
            product_instance = product_data.get('product')

            if not product_instance:
                raise serializers.ValidationError("Product does not exist.")

            # OrderItem.objects.create(
            #     order=order,
            #     product=product_instance,  # Use product_id instead of product
            #     quantity=product_data.get('quantity', 1)
            # )

        return order
