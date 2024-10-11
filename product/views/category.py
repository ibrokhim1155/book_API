from django.views.decorators.cache import cache_page
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from product.models import Category
from product.serializers import CategoriesGroupsProductsSerializer
from product.permissions import IsOwnerOrReadOnly
from django.utils.decorators import method_decorator


@method_decorator(cache_page(60 * 11), name='dispatch')
class CategoriesDetailListApiView(generics.ListCreateAPIView):
    """Displays a list of categories, allows adding a new category."""
    permission_classes = [AllowAny]
    queryset = Category.objects.prefetch_related(
        'groups',
        'groups__products__comments',
        'groups__products__images',
        'groups__products__users_like'
    )
    serializer_class = CategoriesGroupsProductsSerializer


@method_decorator(cache_page(60 * 11), name='dispatch')
class CategoryDetailApiView(generics.RetrieveUpdateDestroyAPIView):
    """Displays detail of a category, allows update or delete."""
    permission_classes = [AllowAny]
    serializer_class = CategoriesGroupsProductsSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Category.objects.prefetch_related(
            'groups',
            'groups__products__comments',
            'groups__products__users_like'
        ).all()

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


@method_decorator(cache_page(60 * 11), name='dispatch')
class CategoryAddView(generics.CreateAPIView):
    """Allows creating a new category."""
    serializer_class = CategoriesGroupsProductsSerializer
