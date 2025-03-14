from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from api.models import Product, Category
from api.serializers import ProductSerializer, CategorySerializer


# Create your views here.

class ProductList(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)

class ProductDetailView(APIView):
    def get(self,request, pk,format=None):
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def put(self,request,pk,format=None):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk,format=None):
        product = get_object_or_404(Product,pk=pk)
        if product:
            product.delete()
            data = {'Message': 'Product deleted successfully'}
            return Response(data, status=status.HTTP_204_NO_CONTENT)

class ProductCreateView(APIView):
    permission_classes = [AllowAny,]
    def post(self,request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductUpdateView(APIView):
    permission_classes = [AllowAny,]
    def put(self,request,pk,format=None):
        product = get_object_or_404(Product,pk=pk)
        serializer = ProductSerializer(product,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#          Generic
class ProductLists(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetails(GenericAPIView,UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    def put(self, request, pk, format=None,*args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk, format=None):
        products = Product.objects.get(pk=pk)
        products.delete()
        data = {'Message': 'Product deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class ProductCreates(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    def post(self,request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdate(GenericAPIView,UpdateModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get(self, request, pk, format=None):
        products = Product.objects.get(pk=pk)
        serializer = ProductSerializer(products)
        return Response(serializer.data)

    def put(self, request, pk, format=None,*args, **kwargs):
        return self.update(request, *args, **kwargs)



class CategoryList(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryDetail(APIView):
    def get(self, request, pk, format=None):
        categories = Category.objects.get(pk=pk)
        serializer = CategorySerializer(categories)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        categories = get_object_or_404(Category,pk=pk)
        serializer = CategorySerializer(categories,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        categories = get_object_or_404(Category,pk=pk)
        categories.delete()
        data = {'Message': 'Category deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class CategoryCreates(APIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    def post(self,request,format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)