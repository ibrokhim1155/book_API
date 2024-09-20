from django.urls import path
from .views import CategoryAPIView

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryAPIView.as_view(), name='category-detail'),
]
