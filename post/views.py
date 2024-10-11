from django.shortcuts import render
from django.core.cache import cache
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from post.models import Post
from post.serializers import PostSerializer
from post.permissions import MyIsAuthenticated, IsAnnaPermission

class PostListView(ListCreateAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [MyIsAuthenticated]

    def get_queryset(self):
        cache_key = 'post-list'
        cached_data = cache.get(cache_key)
        if not cached_data:
            queryset = Post.objects.select_related('user').all()
            queryset = queryset.prefetch_related('user__groups')
            queryset = queryset.prefetch_related('user__user_permissions')
            cache.set(cache_key, queryset, timeout=60*3)
            return queryset
        return cached_data

class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [IsAnnaPermission]
    lookup_field = 'pk'
