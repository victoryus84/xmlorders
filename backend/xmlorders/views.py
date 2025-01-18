from django.shortcuts import render
from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from .models import Order
from .serializers import UserSerializer, GroupSerializer, OrderSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    queryset = Order.objects.filter(status='pending').order_by('created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def pending(self, request):
        """
        Custom action to get only pending orders.
        """
        pending_orders = Order.objects.filter(status='pending', representative=request.user)
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Custom action to update the status of an order.
        """
        order = self.get_object()
        serializer = OrderStatusSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
