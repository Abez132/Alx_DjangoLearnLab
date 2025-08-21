# API Views Documentation

This document provides detailed information about the generic views implemented for the Book model in the Django REST Framework API.

## Overview

The API implements CRUD operations for the Book model using Django REST Framework's generic views. Each view is designed to handle specific operations with appropriate permissions and validation.

## Views Implementation

### 1. BookListView (ListAPIView)
- **Purpose**: Retrieve all books with filtering, searching, and ordering capabilities
- **Endpoint**: `/api/books/list/`
- **HTTP Method**: GET
- **Permissions**: AllowAny (accessible to all users)
- **Serializer**: BookSerializer
- **Features**: 
  - Read-only access to book list
  - Pagination enabled (10 items per page)
  - Filtering by author, publication year, and custom filters
  - Searching in title and author name
  - Ordering by title and publication year
  - Default ordering by title

#### Filtering Examples:
- Filter by author ID: `/api/books/list/?author=1`
- Filter by publication year: `/api/books/list/?publication_year=2023`
- Filter by author name (case-insensitive): `/api/books/list/?author_name=tolkien`
- Filter by publication year range: `/api/books/list/?publication_year_min=2000&publication_year_max=2023`
- Filter by title containing text: `/api/books/list/?title_contains=django`

#### Searching Examples:
- Search in title and author name: `/api/books/list/?search=django`

#### Ordering Examples:
- Order by title: `/api/books/list/?ordering=title`
- Order by publication year: `/api/books/list/?ordering=publication_year`
- Reverse order: `/api/books/list/?ordering=-publication_year`

### 2. BookDetailView (RetrieveAPIView)
- **Purpose**: Retrieve a single book by ID
- **Endpoint**: `/api/books/<int:pk>/`
- **HTTP Method**: GET
- **Permissions**: AllowAny (accessible to all users)
- **Serializer**: BookSerializer
- **Features**:
  - Read-only access to individual book details
  - Returns 404 if book doesn't exist

### 3. BookCreateView (CreateAPIView)
- **Purpose**: Create a new book
- **Endpoint**: `/api/books/create/`
- **HTTP Method**: POST
- **Permissions**: IsAuthenticated (requires authentication)
- **Serializer**: BookSerializer
- **Features**:
  - Validates publication year (cannot be in the future)
  - Requires authenticated user to create books
  - Returns 201 on successful creation

### 4. BookUpdateView (UpdateAPIView)
- **Purpose**: Update an existing book
- **Endpoints**: 
  - `/api/books/<int:pk>/update/` (recommended - with book ID)
  - `/api/books/update/` (alternative - without book ID, requires ID in request data)
- **HTTP Methods**: PUT/PATCH
- **Permissions**: IsAuthenticated (requires authentication)
- **Serializer**: BookSerializer
- **Features**:
  - Validates publication year (cannot be in the future)
  - Requires authenticated user to modify books
  - Returns 200 on successful update
  - Note: The endpoint without ID in URL requires the book ID to be specified in the request data

### 5. BookDeleteView (DestroyAPIView)
- **Purpose**: Delete a book
- **Endpoints**: 
  - `/api/books/<int:pk>/delete/` (recommended - with book ID)
  - `/api/books/delete/` (alternative - without book ID, requires ID in request data)
- **HTTP Method**: DELETE
- **Permissions**: IsAuthenticated (requires authentication)
- **Serializer**: BookSerializer
- **Features**:
  - Requires authenticated user to delete books
  - Returns 204 on successful deletion
  - Note: The endpoint without ID in URL requires the book ID to be specified in the request data

## Permissions Configuration

The API uses a combination of global and view-level permissions:

1. **Global Settings** (in settings.py):
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 10,
       'DEFAULT_FILTER_BACKENDS': [
           'django_filters.rest_framework.DjangoFilterBackend',
           'rest_framework.filters.SearchFilter',
           'rest_framework.filters.OrderingFilter',
       ]
   }
   ```

2. **View-Level Permissions**:
   Each view explicitly defines its permission classes:
   - `AllowAny` for read-only views (ListView, DetailView)
   - `IsAuthenticated` for write operations (CreateView, UpdateView, DeleteView)

## Customization Details

### Validation
- The BookSerializer includes custom validation to ensure the publication year is not in the future
- This validation is automatically applied during create and update operations

### Custom Methods
- `perform_create()` in BookCreateView allows for additional logic during book creation
- `perform_update()` in BookUpdateView allows for additional logic during book updates

### Custom Filters
- Custom BookFilter class provides advanced filtering capabilities
- Filters include author name (case-insensitive), publication year range, and title search

## Testing the API

You can test these views using tools like Postman or curl:

1. **List all books with filtering** (no authentication required):
   ```bash
   curl -X GET "http://localhost:8000/api/books/list/?author=1&publication_year=2023"
   ```

2. **Search books** (no authentication required):
   ```bash
   curl -X GET "http://localhost:8000/api/books/list/?search=django"
   ```

3. **Order books** (no authentication required):
   ```bash
   curl -X GET "http://localhost:8000/api/books/list/?ordering=-publication_year"
   ```

4. **Get a specific book** (no authentication required):
   ```bash
   curl -X GET http://localhost:8000/api/books/1/
   ```

5. **Create a book** (authentication required):
   ```bash
   curl -X POST http://localhost:8000/api/books/create/ \
        -H "Authorization: Token <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"title": "Sample Book", "publication_year": 2023, "author": 1}'
   ```

6. **Update a book with ID in URL** (authentication required):
   ```bash
   curl -X PUT http://localhost:8000/api/books/1/update/ \
        -H "Authorization: Token <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"title": "Updated Book Title", "publication_year": 2023, "author": 1}'
   ```

7. **Update a book without ID in URL** (authentication required):
   ```bash
   curl -X PUT http://localhost:8000/api/books/update/ \
        -H "Authorization: Token <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"id": 1, "title": "Updated Book Title", "publication_year": 2023, "author": 1}'
   ```

8. **Delete a book with ID in URL** (authentication required):
   ```bash
   curl -X DELETE http://localhost:8000/api/books/1/delete/ \
        -H "Authorization: Token <your_token>"
   ```

9. **Delete a book without ID in URL** (authentication required):
   ```bash
   curl -X DELETE http://localhost:8000/api/books/delete/ \
        -H "Authorization: Token <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"id": 1}'
   ```

## Notes

- All views inherit from DRF's generic views for consistency and maintainability
- The API follows REST conventions for HTTP methods and response codes
- Error handling is automatically provided by DRF generic views
- Pagination is enabled globally for list views
- The endpoints without ID in the URL are provided for flexibility but require the ID to be specified in the request data, which is not a standard REST pattern
- It is recommended to use the endpoints with ID in the URL for update and delete operations as they follow REST conventions
- Filtering, searching, and ordering capabilities are only available on the BookListView