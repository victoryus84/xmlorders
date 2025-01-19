from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
router.register(r'clients', ClientViewSet)
router.register(r'products', ProductViewSet)    
router.register(r'orders', OrderViewSet)