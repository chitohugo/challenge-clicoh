from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Product, Order, OrderDetail


class ProductSerializer(ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'stock', 'user')


class ProductDetailSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'price'
        )


class OrderDetailSerializer(ModelSerializer):
    quantity = serializers.IntegerField(required=True, min_value=1,
                                        max_value=1000)
    product_id = serializers.UUIDField(required=True, write_only=True)
    product = ProductDetailSerializer(read_only=True)

    class Meta:
        model = OrderDetail
        fields = (
            'id',
            'quantity',
            'product',
            'product_id'
        )

    def validate(self, data):
        """
        Verify that there is stock and the product is not repeated.
        """
        instance = Product.objects.filter(id=str(data['product_id'])).first()
        if instance.stock == 0:
            raise serializers.ValidationError("No products available")
        if instance.stock < data['quantity']:
            raise serializers.ValidationError(
                f"Only available {instance.stock} {instance.name}")
        return data


class OrderSerializer(ModelSerializer):
    user = serializers.StringRelatedField()
    order_details = OrderDetailSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'user',
            'get_total',
            'get_total_usd',
            'created_date',
            'order_details',
        )

    def create(self, validated_data):
        order_details = validated_data.pop('order_details')
        instance = Order.objects.create(**validated_data)
        for order_detail in order_details:
            OrderDetail.objects.create(order=instance, **order_detail)
            product = Product.objects.filter(
                id=str(order_detail['product_id'])).first()
            product.stock -= order_detail['quantity']
            product.save()
        return instance

    def update(self, instance, validated_data):
        order_details = instance.order_details.all()
        orders = list(order_details)
        for order_detail in validated_data.pop('order_details'):
            order = orders.pop(0)
            quantity = order.quantity
            order.quantity = order_detail.get('quantity', order.quantity)
            order.product_id = order_detail.get('product_id',
                                                order.product)

            product = Product.objects.filter(
                id=str(order_detail['product_id'])).first()
            if quantity != order_detail['quantity']:
                total = (product.stock + quantity) - order_detail['quantity']
                order.product.stock = total
                product.stock = total
                product.save()
            order.save()
        return instance
