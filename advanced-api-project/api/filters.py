"""
Filters for the API application.

This module defines custom filters for the Book model to provide advanced
filtering capabilities in the API.
"""

import django_filters
from .models import Book, Author


class BookFilter(django_filters.FilterSet):
    """
    Custom filter set for the Book model.
    
    This filter set provides advanced filtering capabilities for the Book model,
    allowing users to filter books by various criteria.
    """
    
    # Custom filter for author name (case-insensitive partial match)
    author_name = django_filters.CharFilter(
        field_name='author__name',
        lookup_expr='icontains',
        label='Author name contains'
    )
    
    # Custom filter for books published in a specific year range
    publication_year_min = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='gte',
        label='Publication year from'
    )
    
    publication_year_max = django_filters.NumberFilter(
        field_name='publication_year',
        lookup_expr='lte',
        label='Publication year to'
    )
    
    # Custom filter for books with titles containing specific text (case-insensitive)
    title_contains = django_filters.CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Title contains'
    )
    
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains'],
            'publication_year': ['exact', 'gte', 'lte'],
            'author': ['exact'],
        }