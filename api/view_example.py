import requests
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView, RetrieveUpdateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from api.models import Product, Category, Comment
from api.serializers import ProductSerializer, CategorySerializer, CommentSerializer
from bs4 import BeautifulSoup
from rest_framework.response import Response
from rest_framework.views import APIView
from api.permissions import GetOrPostPermission, UpdateTimePermission


class ExitAPI(APIView):
    def get(self, request):
        url = "https://tuitkf.uz/en/"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data"}, status=response.status_code)

        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "title": soup.title.string if soup.title else "No title",
            "h1": [h1.text.strip() for h1 in soup.find_all("h1")],
            "links": [a["href"] for a in soup.find_all("a", href=True)]
        }

        return Response(data)

# --------------------------------------------- Product --------------------------------------------------

class ProductList(APIView):
    permission_classes = [AllowAny,]

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


    def post(self,request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailView(APIView):
    permission_classes = [AllowAny,]
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


#----------------------------------------------- Comment -------------------------------------------------

class CommentDetail(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, pk, format=None):
        comments = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comments)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        comments = get_object_or_404(Comment,pk=pk)
        serializer = CommentSerializer(comments,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comments = get_object_or_404(Comment,pk=pk)
        comments.delete()
        data = {'Message': 'Comment deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class CommentsLists(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def post(self,request,format=None):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#------------------------------------------ Generic -------------------------------------------------------

#------------------------------------------ Product --------------------------------------------------------
class ProductLists(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request, format=None):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True, context = {"request": request})
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

# ----------------------------------------------------- Category ------------------------------------------------------
class CategoryList(APIView):
    permission_classes = [AllowAny,]
    def get(self, request, format=None):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self,request,format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


#----------------------------------------------- Comment --------------------------------------------------

class CommentDetailByGeneric(GenericAPIView,UpdateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    def get(self, request, pk, format=None):
        comment = Comment.objects.get(pk=pk)
        serializer = CommentSerializer(comment,context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk, format=None,*args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, pk, format=None):
        comments = Comment.objects.get(pk=pk)
        comments.delete()
        data = {'Message': 'Comment deleted successfully'}
        return Response(data, status=status.HTTP_204_NO_CONTENT)


class CommentListsByProduct(ListAPIView):
    serializer_class = CommentSerializer
    def get_queryset(self, *args, **kwargs):
        product = self.kwargs['pk']
        queryset = Comment.objects.filter(product=product)
        return queryset

#---------------------------------------------- Product Old -------------------------------------------------

# class ProductUpdate(GenericAPIView,UpdateModelMixin):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def get(self, request, pk, format=None):
#         products = Product.objects.get(pk=pk)
#         serializer = ProductSerializer(products)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None,*args, **kwargs):
#         return self.update(request, *args, **kwargs)


class ProductUpdateView(RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [UpdateTimePermission]