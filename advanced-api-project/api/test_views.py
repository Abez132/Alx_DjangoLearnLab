"""
Tests for the API views.

This module contains unit tests for the API views, focusing on testing CRUD operations,
filtering, searching, ordering functionalities, and permission enforcement.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from datetime import datetime
from .models import Author, Book
from .serializers import BookSerializer


class BookViewsTest(APITestCase):
    """Test cases for the Book generic views."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpass123'
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
    
    def test_book_list_view_filtering_by_author_name(self):
        """Test filtering books by author name."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'author_name': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Test Book")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Test Book")
    
    def test_book_list_view_filtering_by_publication_year_range(self):
        """Test filtering books by publication year range."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'publication_year_min': 2020, 'publication_year_max': 2022})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Another Book")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Another Book")
    
    def test_book_list_view_filtering_by_title_contains(self):
        """Test filtering books by title containing specific text."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'title_contains': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
            self.assertEqual(response.data['results'][0]['title'], "Test Book")
        else:
            self.assertEqual(len(response.data), 1)
            self.assertEqual(response.data[0]['title'], "Test Book")
    
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
    
    def test_book_list_view_reverse_ordering(self):
        """Test reverse ordering books by publication year."""
        url = reverse('book-list-view')
        response = self.client.get(url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check if response is paginated
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 2)
            # Books should be ordered by publication year descending
            self.assertEqual(response.data['results'][0]['publication_year'], 2023)
            self.assertEqual(response.data['results'][1]['publication_year'], 2022)
        else:
            self.assertEqual(len(response.data), 2)
            # Books should be ordered by publication year descending
            self.assertEqual(response.data[0]['publication_year'], 2023)
            self.assertEqual(response.data[1]['publication_year'], 2022)
    
    def test_book_detail_view(self):
        """Test the BookDetailView returns a specific book."""
        url = reverse('book-detail-view', kwargs={'pk': self.book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Test Book")
        self.assertEqual(response.data['publication_year'], 2023)
        self.assertEqual(response.data['author'], self.author.pk)
    
    def test_book_detail_view_not_found(self):
        """Test the BookDetailView returns 404 for non-existent book."""
        url = reverse('book-detail-view', kwargs={'pk': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
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
        self.assertEqual(response.data['title'], 'New Book')
        self.assertEqual(response.data['publication_year'], 2023)
        self.assertEqual(response.data['author'], self.author.pk)
        # Refresh from database to get updated count
        self.assertEqual(Book.objects.count(), 3)
        # Verify the book was actually created in the database
        new_book = Book.objects.get(title='New Book')
        self.assertEqual(new_book.title, 'New Book')
        self.assertEqual(new_book.publication_year, 2023)
        self.assertEqual(new_book.author, self.author)
    
    def test_book_create_view_invalid_data(self):
        """Test that BookCreateView rejects invalid data."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create-view')
        # Try to create a book with a future publication year
        future_year = datetime.now().year + 1
        data = {
            'title': 'Future Book',
            'publication_year': future_year,
            'author': self.author.pk
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verify the book was not created in the database
        self.assertEqual(Book.objects.filter(title='Future Book').count(), 0)
    
    def test_book_create_view_missing_data(self):
        """Test that BookCreateView rejects requests with missing data."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-create-view')
        # Try to create a book without required fields
        data = {
            'title': 'Incomplete Book'
            # Missing publication_year and author
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
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
            'publication_year': 2024,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Updated Book')
        self.assertEqual(response.data['publication_year'], 2024)
        # Refresh from database to verify changes
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')
        self.assertEqual(self.book.publication_year, 2024)
    
    def test_book_update_view_partial_update(self):
        """Test that authenticated users can partially update books."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-update-view', kwargs={'pk': self.book.pk})
        data = {
            'title': 'Partially Updated Book'
            # Not updating publication_year or author
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Partially Updated Book')
        # Refresh from database to verify changes
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Partially Updated Book')
        # Other fields should remain unchanged
        self.assertEqual(self.book.publication_year, 2023)
    
    def test_book_update_view_not_found(self):
        """Test that BookUpdateView returns 404 for non-existent book."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-update-view', kwargs={'pk': 9999})
        data = {
            'title': 'Updated Book',
            'publication_year': 2023,
            'author': self.author.pk
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
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
        # Verify the book was actually deleted from the database
        self.assertEqual(Book.objects.count(), 1)
        # The remaining book should be book2
        remaining_book = Book.objects.first()
        self.assertEqual(remaining_book.title, "Another Book")
    
    def test_book_delete_view_not_found(self):
        """Test that BookDeleteView returns 404 for non-existent book."""
        self.client.login(username='testuser', password='testpass123')
        url = reverse('book-delete-view', kwargs={'pk': 9999})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)