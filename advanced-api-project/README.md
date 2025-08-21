# Advanced API Project

This project demonstrates a Django REST Framework API with custom serializers that handle complex data structures and nested relationships.

## Project Overview

The project includes:
- Django models for `Author` and `Book` with a one-to-many relationship
- Custom serializers with nested object handling
- Data validation for business rules (publication year cannot be in the future)
- Generic views for CRUD operations with proper permissions
- Advanced query capabilities (filtering, searching, and ordering)
- Comprehensive documentation for models, serializers, and views

## Project Structure

```
advanced-api-project/
├── advanced_api_project/          # Project configuration
│   ├── __init__.py
│   ├── settings.py               # Project settings
│   ├── urls.py                   # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── api/                          # Main application
│   ├── __init__.py
│   ├── admin.py                  # Admin interface configuration
│   ├── apps.py
│   ├── models.py                 # Data models (Author, Book)
│   ├── serializers.py            # Custom serializers
│   ├── views.py                  # API views
│   ├── filters.py                # Custom filters
│   ├── urls.py                   # App URL routing
│   ├── tests.py                  # Unit tests
│   └── migrations/               # Database migrations
│       └── __init__.py
├── manage.py                     # Django management script
└── requirements.txt              # Project dependencies
```

## Models

### Author Model
- `name`: CharField representing the author's name

### Book Model
- `title`: CharField representing the book's title
- `publication_year`: IntegerField representing the publication year
- `author`: ForeignKey to Author model (one-to-many relationship)

## Serializers

### BookSerializer
- Serializes all fields of the Book model
- Includes custom validation to ensure publication_year is not in the future

### AuthorSerializer
- Serializes the author's name
- Includes nested serialization of related books using BookSerializer
- Dynamically serializes related books through the related_name='books'

## Views

The project implements generic views for CRUD operations on the Book model:

### Generic Views
- `BookListView`: Retrieve all books with filtering, searching, and ordering capabilities
- `BookDetailView`: Retrieve a single book by ID (read-only, public access)
- `BookCreateView`: Create a new book (authenticated access only)
- `BookUpdateView`: Update an existing book (authenticated access only)
- `BookDeleteView`: Delete a book (authenticated access only)

For detailed documentation on view configurations, see [README_VIEWS.md](api/README_VIEWS.md)

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Original Endpoints
- `/api/authors/` - List all authors with their books (nested)
- `/api/books/` - List all books

### Generic View Endpoints
- `/api/books/list/` - List all books with filtering, searching, and ordering capabilities (GET)
- `/api/books/<int:pk>/` - Retrieve a specific book (GET)
- `/api/books/create/` - Create a new book (POST)
- `/api/books/update/` - Update a book (PUT/PATCH) - ID in request data
- `/api/books/delete/` - Delete a book (DELETE) - ID in request data
- `/api/books/<int:pk>/update/` - Update a specific book (PUT/PATCH)
- `/api/books/<int:pk>/delete/` - Delete a specific book (DELETE)

### Advanced Query Examples

Filtering:
- Filter by author: `/api/books/list/?author=1`
- Filter by publication year: `/api/books/list/?publication_year=2023`

Searching:
- Search in title and author name: `/api/books/list/?search=django`

Ordering:
- Order by title: `/api/books/list/?ordering=title`
- Order by publication year: `/api/books/list/?ordering=publication_year`

For detailed information about each endpoint, permissions, and testing instructions, see [README_VIEWS.md](api/README_VIEWS.md)

## Testing

Run tests with:
```bash
python manage.py test
```

## Validation

The BookSerializer includes custom validation to ensure the publication_year is not in the future. This is implemented in the `validate_publication_year` method.