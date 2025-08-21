"""
Models for the API application.

This module defines the data models for the advanced API project:
- Author: Represents book authors
- Book: Represents books with a relationship to authors

The models establish a one-to-many relationship where one Author can have multiple Books.
"""

from django.db import models


class Author(models.Model):
    """
    Author model representing a book author.
    
    Attributes:
        name (str): The name of the author, limited to 100 characters.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        """String representation of the Author model."""
        return self.name
    
    class Meta:
        """Meta options for the Author model."""
        ordering = ['name']


class Book(models.Model):
    """
    Book model representing a book with an author relationship.
    
    Attributes:
        title (str): The title of the book, limited to 200 characters.
        publication_year (int): The year the book was published.
        author (Author): ForeignKey relationship to the Author model.
        
    The relationship between Author and Book is a one-to-many relationship:
    - One Author can have many Books
    - One Book belongs to one Author
    - This is implemented using a ForeignKey from Book to Author
    - The related_name='books' allows for reverse lookups (author.books.all())
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    def __str__(self):
        """String representation of the Book model."""
        return f"{self.title} ({self.publication_year})"
    
    class Meta:
        """Meta options for the Book model."""
        ordering = ['title']