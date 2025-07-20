from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.list_books, name='list-books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
]
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('relationship/', include('relationship_app.urls')),
]
from django.urls import path
from .views import list_books, LibraryDetailView

urlpatterns = [
    path('books/', list_books, name='book-list'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library-detail'),
]