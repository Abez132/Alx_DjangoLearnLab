"""
Views for the API application.

This module defines the API views for the advanced API project.
Currently contains placeholder views that can be expanded as needed.
"""

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


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