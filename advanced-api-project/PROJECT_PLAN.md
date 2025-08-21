# Advanced API Project Plan

## Project Structure
```
advanced-api-project/
├── advanced_api_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── api/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
│       └── __init__.py
├── manage.py
└── requirements.txt
```

## Implementation Steps

### 1. Environment Setup
- Install Django and Django REST Framework
- Create requirements.txt file with:
  ```
  Django>=4.2
  djangorestframework>=3.14
  ```

### 2. Project Initialization
- Create Django project: `django-admin startproject advanced_api_project .`
- Create Django app: `python manage.py startapp api`

### 3. Configuration
- Update `advanced_api_project/settings.py`:
  - Add `rest_framework` and `api` to `INSTALLED_APPS`
  - Configure database settings (SQLite for simplicity)

### 4. Model Development
- Define `Author` model in `api/models.py`:
  - `name` field (CharField)
- Define `Book` model in `api/models.py`:
  - `title` field (CharField)
  - `publication_year` field (IntegerField)
  - `author` field (ForeignKey to Author)
- Add model documentation

### 5. Serializer Development
- Create `api/serializers.py`:
  - `BookSerializer` with all fields
  - `AuthorSerializer` with nested `BookSerializer`
  - Custom validation for `publication_year` (not in future)
- Add serializer documentation

### 6. Database Migration
- Run `python manage.py makemigrations`
- Run `python manage.py migrate`

### 7. Testing
- Test models and serializers using Django shell
- Verify nested serialization works correctly
- Verify validation works correctly

## Detailed Requirements

### Models
1. **Author Model**
   - Fields:
     - `name`: CharField(max_length=100)

2. **Book Model**
   - Fields:
     - `title`: CharField(max_length=200)
     - `publication_year`: IntegerField()
     - `author`: ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

### Serializers
1. **BookSerializer**
   - Serialize all fields of Book model
   - Custom validation to ensure publication_year is not in the future

2. **AuthorSerializer**
   - Serialize name field
   - Nested serialization of related books using BookSerializer
   - Should dynamically serialize related books

### Documentation
- Add detailed comments in models.py explaining:
  - Purpose of each model
  - Relationship between Author and Book
- Add detailed comments in serializers.py explaining:
  - Purpose of each serializer
  - How nested relationships are handled
  - Validation logic