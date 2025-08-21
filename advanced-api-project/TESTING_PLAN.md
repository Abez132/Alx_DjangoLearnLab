# Testing Plan

## Manual Testing Using Django Shell

### Test Data Creation
1. Create Author instances:
   ```python
   from api.models import Author, Book
   author = Author.objects.create(name="Jane Doe")
   ```

2. Create Book instances:
   ```python
   from datetime import datetime
   book = Book.objects.create(
       title="Sample Book",
       publication_year=datetime.now().year,
       author=author
   )
   ```

### Model Testing
1. Verify Author model creation:
   ```python
   Author.objects.all()
   author = Author.objects.get(name="Jane Doe")
   ```

2. Verify Book model creation:
   ```python
   Book.objects.all()
   book = Book.objects.get(title="Sample Book")
   ```

3. Verify relationships:
   ```python
   author.books.all()  # Should return all books by this author
   book.author  # Should return the author of this book
   ```

### Serializer Testing
1. Test BookSerializer:
   ```python
   from api.serializers import BookSerializer
   serializer = BookSerializer(book)
   print(serializer.data)
   ```

2. Test AuthorSerializer:
   ```python
   from api.serializers import AuthorSerializer
   serializer = AuthorSerializer(author)
   print(serializer.data)  # Should include nested books
   ```

3. Test validation:
   ```python
   from datetime import datetime
   future_year = datetime.now().year + 1
   book_data = {
       'title': 'Future Book',
       'publication_year': future_year,
       'author': author.id
   }
   serializer = BookSerializer(data=book_data)
   serializer.is_valid()  # Should return False
   print(serializer.errors)  # Should show validation error
   ```

## Expected Output Examples

### AuthorSerializer Output
```json
{
  "id": 1,
  "name": "Jane Doe",
  "books": [
    {
      "id": 1,
      "title": "Sample Book",
      "publication_year": 2023,
      "author": 1
    }
  ]
}
```

### BookSerializer Output
```json
{
  "id": 1,
  "title": "Sample Book",
  "publication_year": 2023,
  "author": 1
}
```

## Test Cases

### Valid Data
1. Create author with valid name
2. Create book with valid title and publication year
3. Serialize author with nested books
4. Serialize book

### Invalid Data
1. Try to create book with future publication year (should fail validation)
2. Try to create book without required fields (should fail validation)

### Edge Cases
1. Author with no books (books array should be empty)
2. Multiple books by same author
3. Books by different authors