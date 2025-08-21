"""
Admin configuration for the API application.

This module registers the Author and Book models with the Django admin interface
to allow for easy management of data through the admin panel.
"""

from django.contrib import admin
from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Author model.
    
    This class customizes the Django admin interface for the Author model,
    providing a list display and search functionality.
    """
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin interface configuration for the Book model.
    
    This class customizes the Django admin interface for the Book model,
    providing a list display, filtering, and search functionality.
    """
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('author', 'publication_year')
    search_fields = ('title', 'author__name')