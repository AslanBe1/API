from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

app_name = 'customers'

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [ 
    path('',include(router.urls)),

]