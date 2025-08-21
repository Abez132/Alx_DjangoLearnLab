"""
Tests for the API application.

This module contains unit tests for the models and serializers in the API app.
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from datetime import datetime
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer


class AuthorModelTest(TestCase):
    """Test cases for the Author model."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
    
    def test_author_creation(self):
        """Test that an author can be created."""
        self.assertIsInstance(self.author, Author)
        self.assertEqual(self.author.name, "Test Author")
    
    def test_author_string_representation(self):
        """Test the string representation of the Author model."""
        self.assertEqual(str(self.author), "Test Author")


class BookModelTest(TestCase):
    """Test cases for the Book model."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
    
    def test_book_creation(self):
        """Test that a book can be created."""
        self.assertIsInstance(self.book, Book)
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.publication_year, 2023)
        self.assertEqual(self.book.author, self.author)
    
    def test_book_string_representation(self):
        """Test the string representation of the Book model."""
        self.assertEqual(str(self.book), "Test Book (2023)")
    
    def test_book_author_relationship(self):
        """Test the relationship between Book and Author."""
        self.assertEqual(self.author.books.count(), 1)
        self.assertEqual(self.author.books.first(), self.book)


class BookSerializerTest(TestCase):
    """Test cases for the BookSerializer."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
        self.book_data = {
            'title': 'Test Book',
            'publication_year': 2023,
            'author': self.author.id
        }
    
    def test_book_serializer_valid_data(self):
        """Test that the BookSerializer works with valid data."""
        serializer = BookSerializer(data=self.book_data)
        self.assertTrue(serializer.is_valid())
        book = serializer.save()
        self.assertEqual(book.title, self.book_data['title'])
    
    def test_book_serializer_future_year_validation(self):
        """Test that the BookSerializer validates against future years."""
        future_year = datetime.now().year + 1
        invalid_data = self.book_data.copy()
        invalid_data['publication_year'] = future_year
        
        serializer = BookSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('publication_year', serializer.errors)


class AuthorSerializerTest(TestCase):
    """Test cases for the AuthorSerializer."""
    
    def setUp(self):
        """Set up test data."""
        self.author = Author.objects.create(name="Test Author")
    
    def test_author_serializer_with_no_books(self):
        """Test that the AuthorSerializer works with no books."""
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        self.assertEqual(data['name'], "Test Author")
        self.assertEqual(data['books'], [])
    
    def test_author_serializer_with_books(self):
        """Test that the AuthorSerializer includes nested books."""
        book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
        
        serializer = AuthorSerializer(self.author)
        data = serializer.data
        self.assertEqual(data['name'], "Test Author")
        self.assertEqual(len(data['books']), 1)
        self.assertEqual(data['books'][0]['title'], "Test Book")