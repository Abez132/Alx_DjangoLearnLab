"""
Tests for the API application.

This module contains unit tests for the models, serializers, and views in the API app.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
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


class BookViewsTest(APITestCase):
    """Test cases for the Book generic views."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.author = Author.objects.create(name="Test Author")
        self.book = Book.objects.create(
            title="Test Book",
            publication_year=2023,
            author=self.author
        )
        # Create another author and book for filtering tests
        self.author2 = Author.objects.create(name="Another Author")
        self.book2 = Book.objects.create(
            title="Another Book",
            publication_year=2022,
            author=self.author2
        )
    
    def test_book_list_view(self):
        """Test the BookListView returns all books."""
        url = reverse('book-list-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
        else:
            self.assertEqual(len(response.data), 2)
    
    def test_book_list_view_filtering_by_author(self):
        """Test filtering books by author."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'author': self.author.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Test Book")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Test Book")
    
    def test_book_list_view_filtering_by_publication_year(self):
        """Test filtering books by publication year."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'publication_year': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Another Book")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Another Book")
    
    def test_book_list_view_searching(self):
        """Test searching books by title or author name."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Test Book")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Test Book")
    
    def test_book_list_view_ordering(self):
        """Test ordering books by title."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
            # Books should be ordered alphabetically by title
            self.assertEqual(response.data['results'][0]['title'], "Another Book")
            self.assertEqual(response.data['results'][1]['title'], "Test Book")
        else:
            self.assertEqual(len(response.data), 2)
            # Books should be ordered alphabetically by title
            self.assertEqual(response.data[0]['title'], "Another Book")
            self.assertEqual(response.data[1]['title'], "Test Book")
    
    def test_book_detail_view(self):
        """Test the BookDetailView returns a specific book."""
        url = reverse('book-detail-view', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")
    
    def test_book_create_view_unauthenticated(self):
        """Test that BookCreateView requires authentication."""
        url = reverse('book-create-view')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_create_view_authenticated(self):
        """Test that authenticated users can create books."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create-view')
        data = {
            'title': 'New Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Refresh from database to get updated count
        self.assertEqual(Book.objects.count(), 3)
        # Get the most recently created book
        new_book = Book.objects.order_by('-id').first()
        self.assertEqual(new_book.title, 'New Book')
    
    def test_book_update_view_unauthenticated(self):
        """Test that BookUpdateView requires authentication."""
        url = reverse('book-update-view', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_update_view_authenticated(self):
        """Test that authenticated users can update books."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-update-view', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Updated Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
    
    def test_book_delete_view_unauthenticated(self):
        """Test that BookDeleteView requires authentication."""
        url = reverse('book-delete-view', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_book_delete_view_authenticated(self):
        """Test that authenticated users can delete books."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-delete-view', kwargs={'pk': self.book.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)