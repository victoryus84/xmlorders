from django.contrib.auth.models import Group, User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

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
    items = OrderItemSerializer(source='orderitem_set', many=True)
    client = ClientSerializer()
    representative = UserSerializer()

    class Meta:
        model = Order
        fields = ['id', 'representative', 'client', 'status', 'created_at', 'items']                

    def create(self, validated_data):
        items_data = validated_data.pop('orderitem_set')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order

    def update(self, instance, validated_data):
        items_data = validated_data.pop('orderitem_set')
        instance.representative = validated_data.get('representative', instance.representative)
        instance.client = validated_data.get('client', instance.client)
        instance.status = validated_data.get('status', instance.status)
        instance.save()

        for item_data in items_data:
            item_id = item_data.get('id')
            if item_id:
                item = OrderItem.objects.get(id=item_id, order=instance)
                item.quantity = item_data.get('quantity', item.quantity)
                item.price = item_data.get('price', item.price)
                item.sum = item_data.get('sum', item.sum)
                item.save()
            else:
                OrderItem.objects.create(order=instance, **item_data)

        return instance    

class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']