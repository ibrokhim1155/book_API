from django.urls import path
from post.views import PostListView, PostDetailApiView

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailApiView.as_view(), name='post-detail'),
]
