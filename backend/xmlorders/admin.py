from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
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

# Определите функцию для создания токена
def generate_token(modeladmin, request, queryset):
    """
    Генерирует токен для выбранных пользователей.
    """
    for user in queryset:
        token, created = Token.objects.get_or_create(user=user)
        modeladmin.message_user(request, f"Токен для пользователя {user.username}: {token.key}")

generate_token.short_description = "Создать токен для выбранных пользователей"

# Создайте кастомный класс администратора для пользователей
class CustomUserAdmin(UserAdmin):
    list_display = (*UserAdmin.list_display, 'has_token')  # Добавляем столбец "has_token"
    actions = [generate_token]  # Добавляем действие для генерации токенов

    def has_token(self, obj):
        """
        Проверяет, существует ли токен для пользователя.
        """
        return Token.objects.filter(user=obj).exists()
    has_token.boolean = True
    has_token.short_description = "Есть токен?"

# Регистрируйте кастомный класс вместо стандартного
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)