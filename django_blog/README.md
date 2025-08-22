# Django Blog Project

This is a simple Django blog project created as part of the ALX Django learning lab.

## Project Overview

The project includes:
- A Django project named `django_blog`
- A Django app named `blog`
- A `Post` model with title, content, published_date, and author fields
- Basic templates for displaying blog posts
- Static files (CSS, JavaScript)
- Django admin configuration for managing blog posts

## Project Structure

```
django_blog/
├── django_blog/          # Project configuration
│   ├── __init__.py
│   ├── settings.py       # Project settings
│   ├── urls.py           # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── blog/                 # Main application
│   ├── __init__.py
│   ├── admin.py          # Admin interface configuration
│   ├── apps.py
│   ├── models.py         # Data models (Post)
│   ├── views.py          # Views
│   ├── urls.py           # App URL routing
│   └── migrations/       # Database migrations
│       └── __init__.py
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   └── blog/             # Blog templates
│       └── post_list.html # Post list template
├── static/               # Static files
│   ├── css/              # CSS files
│   │   └── style.css     # Main stylesheet
│   ├── js/               # JavaScript files
│   │   └── script.js     # Main JavaScript file
│   └── images/           # Image files
├── manage.py             # Django management script
└── README.md             # This file
```

## Setup Instructions

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install Django:
   ```bash
   pip install django
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

6. Open a browser and go to http://127.0.0.1:8000/ to see the blog

## Models

### Post Model
- `title`: CharField representing the post title (max 200 characters)
- `content`: TextField representing the post content
- `published_date`: DateTimeField representing when the post was published (auto-set)
- `author`: ForeignKey to Django's User model (one-to-many relationship)

## Admin Interface

The Post model is registered in the Django admin with:
- List display of title, author, and published_date
- Filtering by published_date and author
- Search functionality for title and content
- Ordering by published_date (descending)
- Date hierarchy navigation

## Templates

- `base.html`: Base template with common HTML structure
- `blog/post_list.html`: Template for displaying a list of blog posts

## Static Files

- `css/style.css`: Basic styling for the blog
- `js/script.js`: Basic JavaScript functionality
- `images/`: Directory for image files (currently empty)