from rest_framework import generics, status
from rest_framework.response import Response
from product import serializers
from product.models import Product, AttributeKey, AttributeValue, ProductAttributeValue
from django.http import Http404


class ProductsListApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        try:
            return super().get_object()
        except Product.DoesNotExist:
            raise Http404("Product not found.")

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductAddView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer


class AttributeKeyListApiView(generics.ListCreateAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = serializers.AttributeKeySerializer


class AttributeValueListApiView(generics.ListCreateAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = serializers.AttributeValueSerializer


class AttributeKeyValueListApiView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = serializers.AttributeKeyValueSerializer
