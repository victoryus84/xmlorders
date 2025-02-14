from django.urls import include, path
from .routers import router

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include('rest_framework.urls', namespace='rest_framework')),
]