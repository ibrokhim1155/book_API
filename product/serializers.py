from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    full_image_url = serializers.SerializerMethodField()
    count = serializers.SerializerMethodField(method_name='groups_count')

    def groups_count(self, obj):
        return obj.groups.count()

    def get_full_image_url(self, instance):
        if instance.image:
            request = self.context.get('request')
            return request.build_absolute_uri(instance.image.url)
        return None

    class Meta:
        model = Category
        fields = ['id', 'title', 'full_image_url', 'count']


class ProductSerializer(serializers.ModelSerializer):
    full_image_url = serializers.SerializerMethodField()

    def get_full_image_url(self, instance):
        if instance.image:
            request = self.context.get('request')
            return request.build_absolute_uri(instance.image.url)
        return None

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'price', 'quantity', 'slug', 'group', 'full_image_url']
