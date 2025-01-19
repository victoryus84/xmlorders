from django.contrib import admin
from .models import *

admin.site.register(Client)
admin.site.register(Category)
admin.site.register(Product)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields = ['representative', 'created_at']
    inlines = [OrderItemInline]

admin.site.register(Order, OrderAdmin)