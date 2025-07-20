from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library, Author  # Now properly importing all needed models

# Function-based view to list all books
def list_books(request):
    """
    Function-based view that displays all books in the system
    Returns:
        Rendered template with list of all books and their authors
    """
    books = Book.objects.all().select_related('author')  # Optimized query
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """
    Class-based view that shows details of a specific library
    including all books available in that library
    """
    model = Library  # This is why we need the Library import
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        """Optimized query with prefetching of related books and authors"""
        return super().get_queryset().prefetch_related('books__author')

    def get_context_data(self, **kwargs):
        """Adds additional context data to the template"""
        context = super().get_context_data(**kwargs)
        # You can add extra context here if needed
        return context