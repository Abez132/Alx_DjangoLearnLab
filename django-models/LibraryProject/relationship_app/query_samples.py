from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    # Create authors
    author1 = Author.objects.create(name="J.K. Rowling")
    author2 = Author.objects.create(name="George R.R. Martin")
    
    # Create books
    book1 = Book.objects.create(title="Harry Potter and the Philosopher's Stone", author=author1)
    book2 = Book.objects.create(title="A Game of Thrones", author=author2)
    book3 = Book.objects.create(title="Harry Potter and the Chamber of Secrets", author=author1)
    
    # Create libraries
    library1 = Library.objects.create(name="Central Library")
    library2 = Library.objects.create(name="City Public Library")
    
    # Add books to libraries
    library1.books.add(book1, book2)
    library2.books.add(book2, book3)
    
    # Create librarians
    librarian1 = Librarian.objects.create(name="Sarah Johnson", library=library1)
    librarian2 = Librarian.objects.create(name="Michael Brown", library=library2)
    
    return {
        "authors": [author1, author2],
        "books": [book1, book2, book3],
        "libraries": [library1, library2],
        "librarians": [librarian1, librarian2]
    }

def query_all_books_by_author(author_name):
    """Query all books by a specific author"""
    author = Author.objects.get(name=author_name)
    books = Book.objects.filter(author=author)
    print(f"\nAll books by {author_name}:")
    for book in books:
        print(f"- {book.title}")
    return books

def list_all_books_in_library(library_name):
    """List all books in a library"""
    library = Library.objects.get(name=library_name)
    books = library.books.all()
    print(f"\nAll books in {library_name}:")
    for book in books:
        print(f"- {book.title} (by {book.author.name})")
    return books

def get_librarian_for_library(library_name):
    """Retrieve the librarian for a library using different query methods"""
    # Method 1: Using library__name lookup
    librarian1 = Librarian.objects.get(library__name=library_name)
    
    # Method 2: First get library, then get librarian
    library = Library.objects.get(name=library_name)
    librarian2 = Librarian.objects.get(library=library)
    
    # Verify both methods return same librarian
    assert librarian1 == librarian2
    
    print(f"\nLibrarian for {library_name} (using both query methods):")
    print(f"- Method 1 (library__name): {librarian1.name}")
    print(f"- Method 2 (library object): {librarian2.name}")
    
    return {
        'by_library_name': librarian1,
        'by_library_obj': librarian2
    }

def run_all_queries():
    # First create sample data
    data = create_sample_data()
    
    # Run all the query examples
    query_all_books_by_author("J.K. Rowling")
    list_all_books_in_library("Central Library")
    get_librarian_for_library("City Public Library")

if __name__ == "__main__":
    run_all_queries()