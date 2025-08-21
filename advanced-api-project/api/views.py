"""
Views for the API application.

This module defines the API views for the advanced API project.
Currently contains placeholder views that can be expanded as needed.
"""

from django.shortcuts import render
from django_filters import rest_framework as django_filters
from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django_filters.rest_framework import DjangoFilterBackend
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer
from .filters import BookFilter


# Placeholder views - these can be expanded based on project requirements


@api_view(['GET'])
def author_list(request):
    """
    List all authors with their books (nested serialization).
    
    This view demonstrates the nested serialization functionality
    where each author includes their related books.
    """
    authors = Author.objects.all()
    serializer = AuthorSerializer(authors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def book_list(request):
    """
    List all books.
    
    This view demonstrates the book serialization with validation.
    """
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


# Generic views for Book model CRUD operations

class BookListView(generics.ListAPIView):
    """
    Generic view to retrieve all books with filtering, searching, and ordering capabilities.
    
    This view uses DRF's ListAPIView which provides a read-only endpoint
    for listing book instances. It's accessible to all users (authenticated
    and unauthenticated).
    
    Filtering:
    - Filter by author: /api/books/list/?author=1
    - Filter by publication year: /api/books/list/?publication_year=2023
    - Filter by author name: /api/books/list/?author_name=tolkien
    - Filter by publication year range: /api/books/list/?publication_year_min=2000&publication_year_max=2023
    - Filter by title containing text: /api/books/list/?title_contains=django
    
    Searching:
    - Search in title and author name: /api/books/list/?search=django
    
    Ordering:
    - Order by title: /api/books/list/?ordering=title
    - Order by publication year: /api/books/list/?ordering=publication_year
    - Reverse order: /api/books/list/?ordering=-publication_year
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]
    
    # Add filtering, searching, and ordering capabilities
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # Filtering configuration with custom filter
    filterset_class = BookFilter
    
    # Search configuration
    search_fields = ['title', 'author__name']
    
    # Ordering configuration
    ordering_fields = ['title', 'publication_year']
    ordering = ['title']  # default ordering


class BookDetailView(generics.RetrieveAPIView):
    """
    Generic view to retrieve a single book by ID.
    
    This view uses DRF's RetrieveAPIView which provides a read-only endpoint
    for retrieving a specific book instance by its primary key. It's accessible
    to all users (authenticated and unauthenticated).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Generic view to create a new book.
    
    This view uses DRF's CreateAPIView which provides a create-only endpoint
    for adding new book instances. It requires authentication to access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Save the book instance with additional custom logic if needed.
        """
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    """
    Generic view to update an existing book.
    
    This view uses DRF's UpdateAPIView which provides an update-only endpoint
    for modifying existing book instances. It requires authentication to access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        """
        Update the book instance with additional custom logic if needed.
        """
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    """
    Generic view to delete a book.
    
    This view uses DRF's DestroyAPIView which provides a delete-only endpoint
    for removing book instances. It requires authentication to access.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]