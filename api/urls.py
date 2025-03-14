from django.urls import path
from api import views

app_name = 'customers'

urlpatterns = [
    path('', views.ProductList.as_view(), name='APi'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='ApiDetail'),
    path('product-create/', views.ProductCreateView.as_view(), name='ProductCreate'),
    path('product-update/<int:pk>/', views.ProductUpdateView.as_view(), name='ProductUpdate'),

#    Generic

    path('generic-api/', views.ProductLists.as_view(), name='GenericAPI'),
    path('generic-details/<int:pk>/', views.ProductDetails.as_view(), name='GenericDetailsAPI'),
    path('generic-create/', views.ProductCreates.as_view(), name='GenericCreate'),
    path('generic-update/<int:pk>/', views.ProductUpdate.as_view(), name='GenericUpdate'),

#    Category

    path('category-list/', views.CategoryList.as_view(), name='CategoryList'),
    path('category-details/<int:pk>/', views.CategoryDetail.as_view(), name='CategoryDetails'),
    path('category-create/',views.CategoryCreates.as_view(), name='CategoryCreates'),
]