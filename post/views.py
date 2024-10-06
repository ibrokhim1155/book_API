from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from post.models import Post
from post.serializers import PostSerializer
from post.permissions import MyIsAuthenticated, IsOwner, IsAnnaPermission


class PostListView(ListCreateAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [MyIsAuthenticated]

class PostDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.select_related('user').all()
    serializer_class = PostSerializer
    permission_classes = [IsAnnaPermission]
    lookup_field = 'pk'
