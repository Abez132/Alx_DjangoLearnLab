from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library  # Explicitly importing Library model

def list_books(request):
    """
    Function-based view listing all books with their authors
    """
    books = Book.objects.all().select_related('author')
    return render(request, 'relationship_app/list_books.html', 
                {'books': books})

class LibraryDetailView(DetailView):
    """
    Class-based view displaying details for a specific library
    Requires Library model import to work correctly
    """
    model = Library  # This line requires the Library import
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        """Optimize queries by prefetching related books"""
        return super().get_queryset().prefetch_related('books__author')