from django.contrib.auth import authenticate
from rest_framework import permissions, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST
from .models import Order, Client, Product
from .serializers import OrderSerializer, ClientSerializer, ProductSerializer

class Login(APIView):

    """
    Обработка POST-запроса для аутентификации пользователя.

    :param request: Объект запроса, содержащий данные для аутентификации (username и password).
    :return: Возвращает токен аутентификации, если пользователь существует и данные корректны.
            Если данные неверны или пользователь не найден, возвращает ошибку 404.
    """

    def post(self, request):
        username=request.data.get("username")
        password=request.data.get("password")

        if not username or not password:
            return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
        user = authenticate(username=username, password=password)
        if not user:
            return Response({'error': 'Credentials are incorrect or user does not exist'}, status=HTTP_404_NOT_FOUND)
        
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=HTTP_200_OK)
    
class ClientViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint для управления клиентами (CRUD операции).

    - Позволяет создавать, просматривать, обновлять и удалять записи о клиентах.
    - Доступ разрешен только администраторам системы.
    """
    queryset = Client.objects.all().order_by('id')
    serializer_class = ClientSerializer
       
    # Аутентификация через токены.
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint для управления продуктами (CRUD операции).

    - Позволяет создавать, просматривать, обновлять и удалять записи о продуктах.
    - Доступ разрешен только администраторам системы.
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class OrderViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    API endpoint для управления заказами.

    - Позволяет создавать, просматривать, обновлять и удалять записи о заказах.
    - Доступ разрешен только авторизованным пользователям.
    """
    queryset = Order.objects.filter(status='pending').order_by('created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def pending(self, request):
        """
        Получение списка заказов со статусом "в ожидании".

        :param request: Объект запроса.
        :return: Возвращает список заказов, назначенные текущему представителю.
        """
        pending_orders = Order.objects.filter(status='pending', representative=request.user)
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['put'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Обновление статуса заказа.

        :param request: Объект запроса, содержащий новые данные статуса.
        :param pk: Primary key заказа, который нужно обновить.
        :return: Возвращает обновленные данные заказа или ошибку, если данные недопустимы.
        """
        order = self.get_object()
        serializer = OrderStatusSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)    
