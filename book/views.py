from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .models import Book
from django.shortcuts import get_object_or_404


class BooksListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        books = Book.objects.all()
        if not books:
            return Response({"message": "No books found"}, status=status.HTTP_404_NOT_FOUND)

        data = [
            {
                "book_id": book.id,
                "author": book.author,
                "title": book.title,
                "published": book.published_date,
            }
            for book in books
        ]

        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        books_data = request.data
        if isinstance(books_data, list):
            created_books = []
            for book_data in books_data:
                book = Book.objects.create(
                    title=book_data.get('title'),
                    author=book_data.get('author'),
                    published_date=book_data.get('published_date')
                )
                created_books.append({
                    "book_id": book.id,
                    "author": book.author,
                    "title": book.title,
                    "published": book.published_date,
                })
            return Response(created_books, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
