from django.db.models import Avg
from rest_framework import serializers
from product.models import (
    Category, Group, Product,
    ProductAttributeValue, ProductImage,
    Comment
)


class CategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'count']
        read_only_fields = ['id', 'slug']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image']


class ProductCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'rating', 'user', 'image', 'text']
        read_only_fields = ['id']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = ['key', 'value']

    def to_representation(self, instance):
        return {instance.key.key: instance.value.value}


class ProductDetailSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    user_like = serializers.SerializerMethodField()

    def get_user_like(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and obj.users_like.filter(id=request.user.id).exists()

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount', 'quantity', 'slug', 'user_like', 'images',
                  'attributes', 'comments']
        read_only_fields = ['id', 'slug', 'user_like']


class ProductSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    user_like = serializers.SerializerMethodField()
    count_comments = serializers.SerializerMethodField()

    def get_count_comments(self, obj):
        return obj.comments.count()

    def get_avg_rating(self, obj):
        rating = obj.comments.aggregate(avg=Avg('rating'))['avg']
        return rating if rating else 0

    def get_user_like(self, obj):
        request = self.context.get('request')
        return request.user.is_authenticated and obj.users_like.filter(id=request.user.id).exists()

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discount', 'quantity', 'description', 'slug', 'avg_rating', 'user_like',
                  'count_comments', 'group']
        read_only_fields = ['id', 'slug', 'user_like']


class GroupSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Group
        fields = ['id', 'title', 'image', 'slug', 'category', 'products']
        read_only_fields = ['id', 'slug']


class CategoriesGroupsProductsSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'slug', 'groups']
        read_only_fields = ['id', 'slug']
