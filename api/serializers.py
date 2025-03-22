from rest_framework import serializers
from api.models import Product, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='product_count',read_only=True)

    class Meta:
        model = Category
        fields = ['id','name','slug','products_count']


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    comment_count = serializers.IntegerField(source='comments_count',read_only=True)

    category = CategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'discount', 'quantity', 'description',
                  'rating', 'image', 'slug', 'comment_count', 'category', 'category_id']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return None