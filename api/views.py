from django.core.cache import cache,caches
from django.db.models import Count
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from api.models import Product, Category, Comment
from api.permissions import DeleteTimePermission, IsWorkListPermission
from api.serializers import ProductSerializer, CategorySerializer, CommentSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = []
    filterset_fields = ['category','price']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status.HTTP_201_CREATED,headers=headers)

    def get_queryset(self):
        cache_key = 'products/'
        cached_products = cache.get(cache_key)
        if not cached_products:
            cached_products = Product.objects.all().select_related('category')
            cache.set(cache_key, cached_products,timeout=60*2)
        return cached_products

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductViewSet, self).dispatch(request, *args, **kwargs)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = []
    authentication_classes = [TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def get_queryset(self):
        cache_key = 'categories/'
        cached_categories = cache.get(cache_key)
        if not cached_categories:
            cached_categories = Category.objects.all()
            cache.set(cache_key, cached_categories,timeout=60*2)
        return cached_categories

    @method_decorator(cache_page(60))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryViewSet, self).dispatch(request, *args, **kwargs)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    authentication_classes = [JWTAuthentication,]
    # permission_classes = [IsWorkListPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ProductDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [DeleteTimePermission]


class RegisterView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username is taken'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        refresh = RefreshToken.for_user(user)

        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),

        }, status=status.HTTP_200_OK)


class LoginView(APIView):
    authentication_classes = [JWTAuthentication]


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({
            'message': 'Token is blacklisted',
        })