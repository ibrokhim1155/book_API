from rest_framework import generics, status, permissions
from rest_framework.response import Response
from product.serializers import ProductSerializer, ProductDetailSerializer, AttributeKeySerializer, AttributeValueSerializer, AttributeKeyValueSerializer
from product.models import Product, AttributeKey, AttributeValue, ProductAttributeValue
from django.http import Http404


class ProductsListApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'

    def get_object(self):
        try:
            return Product.objects.get(slug=self.kwargs['slug'])
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

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
