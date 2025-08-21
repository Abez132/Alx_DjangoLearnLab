"""
URL configuration for the API application.

This module defines the URL patterns for the API app endpoints.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list, name='author-list'),
    path('books/', views.book_list, name='book-list'),
    
    # Generic views for Book model CRUD operations
    path('books/list/', views.BookListView.as_view(), name='book-list-view'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail-view'),
    path('books/create/', views.BookCreateView.as_view(), name='book-create-view'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book-update-view'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book-delete-view'),
]