from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views
from api import customobtainview
app_name = 'customers'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('',include(router.urls)),
    path('product-delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product-update'),
    path('custom-token/', customobtainview.CustomAuthToken.as_view(), name='custom-token'),
    path('logout-api/',customobtainview.LogoutAPIView.as_view(), name='logout-api'),
    path('register-api/', views.RegisterView.as_view(), name='register-api'),

    # path('api-token-auth/', views.obtain_auth_token)
]