# Testing Examples

This document provides examples of how to test the Django models and serializers using the Django shell.

## Setting Up the Test Environment

1. First, make sure you've run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

2. Start the Django shell:
   ```bash
   python manage.py shell
   ```

## Testing Models

In the Django shell, you can test the models as follows:

```python
# Import the models
from api.models import Author, Book

# Create an author
author = Author.objects.create(name="Jane Doe")
print(author)  # Output: Jane Doe

# Create a book
book = Book.objects.create(
    title="Sample Book",
    publication_year=2023,
    author=author
)
print(book)  # Output: Sample Book (2023)

# Test the relationship
print(author.books.all())  # Output: <QuerySet [<Book: Sample Book (2023)>]>
print(book.author)  # Output: <Author: Jane Doe>

# Create another book by the same author
book2 = Book.objects.create(
    title="Another Book",
    publication_year=2024,
    author=author
)

# Check that both books are associated with the author
print(author.books.count())  # Output: 2
for book in author.books.all():
    print(book.title)  # Output: Sample Book, Another Book
```

## Testing Serializers

In the Django shell, you can test the serializers as follows:

```python
# Import the serializers and models
from api.serializers import AuthorSerializer, BookSerializer
from api.models import Author, Book
from datetime import datetime

# Get an existing author
author = Author.objects.get(name="Jane Doe")

# Test AuthorSerializer (with nested books)
author_serializer = AuthorSerializer(author)
print(author_serializer.data)
# Output: {
#   "id": 1,
#   "name": "Jane Doe",
#   "books": [
#     {
#       "id": 1,
#       "title": "Sample Book",
#       "publication_year": 2023,
#       "author": 1
#     },
#     {
#       "id": 2,
#       "title": "Another Book",
#       "publication_year": 2024,
#       "author": 1
#     }
#   ]
# }

# Get an existing book
book = Book.objects.get(title="Sample Book")

# Test BookSerializer
book_serializer = BookSerializer(book)
print(book_serializer.data)
# Output: {
#   "id": 1,
#   "title": "Sample Book",
#   "publication_year": 2023,
#   "author": 1
# }

# Test BookSerializer validation with valid data
valid_data = {
    'title': 'Valid Book',
    'publication_year': 2023,
    'author': author.id
}
serializer = BookSerializer(data=valid_data)
print(serializer.is_valid())  # Output: True

# Test BookSerializer validation with invalid data (future year)
future_year = datetime.now().year + 1
invalid_data = {
    'title': 'Future Book',
    'publication_year': future_year,
    'author': author.id
}
serializer = BookSerializer(data=invalid_data)
print(serializer.is_valid())  # Output: False
print(serializer.errors)  # Output: {'publication_year': ['Publication year cannot be in the future.']}
```

## Testing API Endpoints

You can also test the API endpoints using curl or a tool like Postman:

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Test the authors endpoint:
   ```bash
   curl http://127.0.0.1:8000/api/authors/
   ```

3. Test the books endpoint:
   ```bash
   curl http://127.0.0.1:8000/api/books/
   ```

## Running Unit Tests

To run the unit tests included in the project:

```bash
python manage.py test
```

This will run all the tests defined in `api/tests.py`, which include:
- Author model tests
- Book model tests
- BookSerializer tests (including validation)
- AuthorSerializer tests (including nested serialization)