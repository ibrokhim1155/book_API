from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from product.models import Category
from product.serializers import CategoriesGroupsProductsSerializer


class CategoriesDetailListApiView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related('groups__products').all()
    serializer_class = CategoriesGroupsProductsSerializer


class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategoriesGroupsProductsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.prefetch_related('groups__products').all()

    def get(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryAddView(generics.CreateAPIView):
    serializer_class = CategoriesGroupsProductsSerializer
