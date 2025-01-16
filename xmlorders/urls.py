from django.urls import include, path
from rest_framework import routers
from .views import UserViewSet, GroupViewSet, OrderViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('api/', include((router.urls, 'api'), namespace='api')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]