"""
URL configuration for the API application.

This module defines the URL patterns for the API app endpoints.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('authors/', views.author_list, name='author-list'),
    path('books/', views.book_list, name='book-list'),
]