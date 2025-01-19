from rest_framework import serializers
from .models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'stock']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'phone', 'address']

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'price', 'sum']

class OrderSerializer(serializers.ModelSerializer):
    client = ClientSerializer()
    representative = serializers.HiddenField(default=serializers.CurrentUserDefault())
    items = OrderItemSerializer(source='orderitem_set', many=True)
   
    class Meta:
        model = Order
        fields = '__all__'                

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']