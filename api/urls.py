from django.urls import path
from api import views

app_name = 'customers'

urlpatterns = [
    path('', views.ProductList.as_view(), name='APi'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='ApiDetail'),

#    Generic

    path('generic-api/', views.ProductLists.as_view(), name='GenericAPI'),
    path('generic-details/<int:pk>/', views.ProductDetails.as_view(), name='GenericDetailsAPI'),

#    Category

    path('category-list/', views.CategoryList.as_view(), name='CategoryList'),
    path('category-details/<int:pk>/', views.CategoryDetail.as_view(), name='CategoryDetails'),

#    Comment
    path('comment/', views.CommentsLists.as_view(), name='Comment'),
    path('comment/<int:pk>/',views.CommentListsByProduct.as_view(), name='CommentsByProduct'),
    path('comment-deteil/<int:pk>/', views.CommentDetailByGeneric.as_view(), name='CommentsDetail'),

#   Tuitkf

    # path('tuitkf/', views.ExitAPI.as_view(), name='tuitkf'),

#   Create and Update Old

    # path('product-create/', views.ProductCreateView.as_view(), name='ProductCreate'),
    path('product-update/<int:pk>/', views.ProductUpdateView.as_view(), name='ProductUpdate'),
    # path('generic-create/', views.ProductCreates.as_view(), name='GenericCreate'),
    # path('generic-update/<int:pk>/', views.ProductUpdate.as_view(), name='GenericUpdate'),
    # path('category-create/',views.CategoryCreates.as_view(), name='CategoryCreates'),

]