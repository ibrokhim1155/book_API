from rest_framework import generics, status
from rest_framework.response import Response
from product.serializers import ProductSerializer, ProductDetailSerializer, AttributeKeySerializer, AttributeValueSerializer, AttributeKeyValueSerializer
from product.models import Product, AttributeKey, AttributeValue, ProductAttributeValue
from django.http import Http404

class ProductsListApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        try:
            return Product.objects.get(slug=self.kwargs.get(self.lookup_field))
        except Product.DoesNotExist:
            raise Http404("Product not found.")

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class ProductAddView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class AttributeKeyListApiView(generics.ListCreateAPIView):
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer

class AttributeValueListApiView(generics.ListCreateAPIView):
    queryset = AttributeValue.objects.all()
    serializer_class = AttributeValueSerializer

class AttributeKeyValueListApiView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = AttributeKeyValueSerializer
