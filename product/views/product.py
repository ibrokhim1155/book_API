from django.http import Http404
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from django.core.cache import cache
from product.serializers import ProductSerializer, ProductDetailSerializer, AttributeKeySerializer
from product.models import Product, AttributeKey

class ProductsListApiView(generics.ListCreateAPIView):
    """ This class used to display all products, and you can add a new product """
    permission_classes = (permissions.AllowAny,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    cache_key = 'products-list'

    def get_queryset(self):
        cached_data = cache.get(self.cache_key)
        if cached_data is not None:
            return cached_data

        queryset = list(super().get_queryset())
        cache.set(self.cache_key, queryset, timeout=60)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        cache.delete(self.cache_key)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """ This class is used to display a detail view of a product,
        additionally you can perform various actions on products
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ProductDetailSerializer
    lookup_field = 'slug'
    cache_key_prefix = 'product-detail-'

    def get_queryset(self):
        return Product.objects.all()

    def get_object(self):
        slug = self.kwargs.get(self.lookup_field)
        cached_object = cache.get(f"{self.cache_key_prefix}{slug}")
        if cached_object is not None:
            return cached_object

        try:
            product = super().get_object()
            cache.set(f"{self.cache_key_prefix}{slug}", product, timeout=60)
            return product
        except Product.DoesNotExist:
            raise Http404("Not found.")

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()
            cache.delete(f"{self.cache_key_prefix}{product.slug}")
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        cache.delete(f"{self.cache_key_prefix}{product.slug}")
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProductAddView(generics.CreateAPIView):
    """ This class is used to add a new product """
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AttributeKeyListApiView(generics.ListCreateAPIView):
    """ This class is used to list all attribute keys and add a new attribute key """
    permission_classes = (permissions.AllowAny,)
    queryset = AttributeKey.objects.all()
    serializer_class = AttributeKeySerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        attribute_key = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
