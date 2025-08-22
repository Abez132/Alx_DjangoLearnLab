from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    """
    Model representing a blog post.
    
    Attributes:
        title (str): The title of the blog post, limited to 200 characters.
        content (str): The content of the blog post.
        published_date (datetime): The date and time when the post was published.
        author (User): The author of the post, linked to Django's User model.
    """
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    
    def __str__(self):
        """String representation of the Post model."""
        return self.title
    
    class Meta:
        """Meta options for the Post model."""
        ordering = ['-published_date']


class Comment(models.Model):
    """
    Model representing a comment on a blog post.
    
    Attributes:
        post (Post): The blog post this comment belongs to.
        author (User): The user who wrote the comment.
        content (str): The content of the comment.
        created_at (datetime): The date and time when the comment was created.
        updated_at (datetime): The date and time when the comment was last updated.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        """String representation of the Comment model."""
        return f'Comment by {self.author.username} on {self.post.title}'
    
    class Meta:
        """Meta options for the Comment model."""
        ordering = ['created_at']