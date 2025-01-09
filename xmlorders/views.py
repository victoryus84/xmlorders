from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm

from rest_framework import viewsets
from .serializers import OrderSerializer

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