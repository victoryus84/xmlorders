from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, User
from .models import Order
from .forms import OrderForm

from rest_framework import permissions, viewsets
from .serializers import *

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
    
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.representative = request.user
            order.save()
            return redirect('order_list')
    else:
        form = OrderForm()
    return render(request, 'orders/create_order.html', {'form': form})

def order_list(request):
    orders = Order.objects.filter(representative=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer