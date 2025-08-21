# Model Design Documentation

## Author Model

### Fields
- `name`: CharField with max_length=100
  - Represents the full name of the author
  - Required field

### Relationships
- One-to-many relationship with Book model
- Related name: 'books' (allows accessing all books by an author via author.books.all())

### Purpose
The Author model represents writers who have authored books in the system. Each author can have multiple books associated with them.

## Book Model

### Fields
- `title`: CharField with max_length=200
  - Represents the title of the book
  - Required field
- `publication_year`: IntegerField
  - Represents the year the book was published
  - Required field
- `author`: ForeignKey to Author model
  - Establishes the one-to-many relationship from Author to Book
  - Uses CASCADE deletion (when an author is deleted, their books are also deleted)
  - Related name: 'books'

### Relationships
- Many-to-one relationship with Author model
- Each book is associated with exactly one author

### Purpose
The Book model represents books in the system. Each book has a title, publication year, and is associated with one author.

## Relationship Explanation
The relationship between Author and Book is a classic one-to-many relationship:
- One Author can have many Books
- One Book belongs to one Author
- This is implemented using a ForeignKey from Book to Author
- The related_name='books' on the ForeignKey allows for reverse lookups (author.books.all())

## Model Diagram
```mermaid
erDiagram
    AUTHOR ||--o{ BOOK : writes
    AUTHOR {
        string name
    }
    BOOK {
        string title
        int publication_year
        int author_id
    }