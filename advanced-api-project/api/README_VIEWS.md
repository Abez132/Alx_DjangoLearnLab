# API Views Documentation

This document provides detailed information about the generic views implemented for the Book model in the Django REST Framework API.

## Overview

The API implements CRUD operations for the Book model using Django REST Framework's generic views. Each view is designed to handle specific operations with appropriate permissions and validation.

## Views Implementation

### 1. BookListView (ListAPIView)
- **Purpose**: Retrieve all books
- **Endpoint**: `/api/books/list/`
- **HTTP Method**: GET
- **Permissions**: AllowAny (accessible to all users)
- **Serializer**: BookSerializer
- **Features**: 
  - Read-only access to book list
  - Pagination enabled (10 items per page)
  - Ordering by title (as defined in the model)

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
- **Endpoint**: `/api/books/<int:pk>/update/`
- **HTTP Method**: PUT/PATCH
- **Permissions**: IsAuthenticated (requires authentication)
- **Serializer**: BookSerializer
- **Features**:
  - Validates publication year (cannot be in the future)
  - Requires authenticated user to modify books
  - Returns 200 on successful update

### 5. BookDeleteView (DestroyAPIView)
- **Purpose**: Delete a book
- **Endpoint**: `/api/books/<int:pk>/delete/`
- **HTTP Method**: DELETE
- **Permissions**: IsAuthenticated (requires authentication)
- **Serializer**: BookSerializer
- **Features**:
  - Requires authenticated user to delete books
  - Returns 204 on successful deletion

## Permissions Configuration

The API uses a combination of global and view-level permissions:

1. **Global Settings** (in settings.py):
   ```python
   REST_FRAMEWORK = {
       'DEFAULT_PERMISSION_CLASSES': [
           'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
       ],
       'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
       'PAGE_SIZE': 10
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

## Testing the API

You can test these views using tools like Postman or curl:

1. **List all books** (no authentication required):
   ```bash
   curl -X GET http://localhost:8000/api/books/list/
   ```

2. **Get a specific book** (no authentication required):
   ```bash
   curl -X GET http://localhost:8000/api/books/1/
   ```

3. **Create a book** (authentication required):
   ```bash
   curl -X POST http://localhost:8000/api/books/create/ \
        -H "Authorization: Token <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"title": "Sample Book", "publication_year": 2023, "author": 1}'
   ```

4. **Update a book** (authentication required):
   ```bash
   curl -X PUT http://localhost:8000/api/books/1/update/ \
        -H "Authorization: Token <your_token>" \
        -H "Content-Type: application/json" \
        -d '{"title": "Updated Book Title", "publication_year": 2023, "author": 1}'
   ```

5. **Delete a book** (authentication required):
   ```bash
   curl -X DELETE http://localhost:8000/api/books/1/delete/ \
        -H "Authorization: Token <your_token>"
   ```

## Notes

- All views inherit from DRF's generic views for consistency and maintainability
- The API follows REST conventions for HTTP methods and response codes
- Error handling is automatically provided by DRF generic views
- Pagination is enabled globally for list views