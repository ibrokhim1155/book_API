from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from product.serializers import GroupSerializer
from product.models import Group


@method_decorator(cache_page(60), name='dispatch')
class GroupDetailListApiView(generics.RetrieveUpdateDestroyAPIView):
    """This class displays detail of a group (products list),
       in this class you can perform various actions on groups."""
    serializer_class = GroupSerializer
    lookup_field = 'slug'

    def get_cache_key(self):
        group_slug = self.kwargs.get('slug')
        return f'group-detail-{group_slug}'

    def get_queryset(self):
        group_slug = self.kwargs.get('slug')
        return Group.objects.prefetch_related('products').filter(
            slug=group_slug
        )

    def get(self, request, *args, **kwargs):
        cache_key = self.get_cache_key()
        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data)

        group = self.get_object()
        serializer = self.get_serializer(group)
        response_data = serializer.data

        cache.set(cache_key, response_data, timeout=60)
        return Response(response_data)

    def put(self, request, *args, **kwargs):
        group = self.get_object()
        serializer = self.get_serializer(group, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        cache.delete(self.get_cache_key())
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        group = self.get_object()
        group.delete()
        cache.delete(self.get_cache_key())
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupAddView(generics.CreateAPIView):
    serializer_class = GroupSerializer
