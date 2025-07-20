from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library  # Explicitly importing Library

# Function-based view to list all books
def list_books(request):
    """Function-based view that lists all books with their authors"""
    books = Book.objects.all().select_related('author')  # Optimized query
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view to display library details
class LibraryDetailView(DetailView):
    """Class-based view showing details of a specific library"""
    model = Library  # This requires the Library import
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    def get_queryset(self):
        """Optimized query with prefetching of related books and authors"""
        return super().get_queryset().prefetch_related('books__author')