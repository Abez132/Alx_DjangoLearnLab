"""
Serializers for the API application.

This module defines the serializers for the advanced API project:
- BookSerializer: Serializes Book model instances with custom validation
- AuthorSerializer: Serializes Author model instances with nested Book serialization

The serializers handle the conversion between Django model instances and JSON representations,
including custom validation logic for business rules.
"""

from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model instances.
    
    This serializer handles serialization and deserialization of Book model instances.
    It includes custom validation to ensure the publication year is not in the future.
    
    Fields:
        All fields from the Book model (title, publication_year, author)
    """
    
    class Meta:
        model = Book
        fields = '__all__'
    
    def validate_publication_year(self, value):
        """
        Custom validation for the publication_year field.
        
        Ensures that the publication year is not in the future.
        
        Args:
            value (int): The publication year to validate
            
        Returns:
            int: The validated publication year
            
        Raises:
            serializers.ValidationError: If the publication year is in the future
        """
        current_year = datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model instances with nested Book serialization.
    
    This serializer handles serialization and deserialization of Author model instances.
    It includes nested serialization of related books using the BookSerializer.
    
    Fields:
        name (str): The name of the author
        books (list): A nested list of books by this author, serialized using BookSerializer
                      This field is read-only and dynamically populated based on the 
                      related_name='books' from the Book model's ForeignKey to Author.
    """
    # Nested serialization of related books
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']