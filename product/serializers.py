from django.db.models import Avg
from rest_framework import serializers
from product.models import (
    Category, Group, Product,
    ProductAttributeValue, ProductImage,
    Comment, AttributeKey, AttributeValue
)


class CategorySerializer(serializers.ModelSerializer):
    groups_count = serializers.SerializerMethodField()

    def get_groups_count(self, obj):
        return obj.groups.count()

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'groups_count']
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
        if instance.key and instance.value:
            return {instance.key.key: instance.value.value}
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    attributes = ProductAttributeValueSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    comments = ProductCommentSerializer(many=True, read_only=True)
    user_like = serializers.SerializerMethodField()

    def get_user_like(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.users_like.filter(id=request.user.id).exists()
        return False

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'discount', 'quantity', 'slug', 'user_like', 'images',
                  'attributes', 'comments']
        read_only_fields = ['id', 'slug', 'user_like']


class ProductSerializer(serializers.ModelSerializer):
    user_like = serializers.SerializerMethodField()
    count_comments = serializers.SerializerMethodField()

    def get_count_comments(self, obj):
        return obj.comments.count()

    def get_user_like(self, obj):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.users_like.filter(id=request.user.id).exists()
        return False

    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'discount', 'quantity', 'description', 'slug', 'average_rating', 'user_like',
                  'count_comments', 'group']
        read_only_fields = ['id', 'slug', 'user_like']


class GroupSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'title', 'image', 'slug', 'category', 'products']
        read_only_fields = ['id', 'slug']


class CategoriesGroupsProductsSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'title', 'image', 'slug', 'groups']
        read_only_fields = ['id', 'slug']


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeKey
        fields = '__all__'


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttributeValue
        fields = '__all__'


class AttributeKeyValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        exclude = ('id', 'product', 'key', 'value')

    def to_representation(self, instance):
        return {
            'key_id': instance.key.id,
            'key_name': instance.key.key,
            'value_id': instance.value.id,
            'value_name': instance.value.value,
        }
