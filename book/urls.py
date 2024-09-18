from django.urls import path
from .views import BooksListView

urlpatterns = [
    path('books/', BooksListView.as_view(), name='books-list'),
]
