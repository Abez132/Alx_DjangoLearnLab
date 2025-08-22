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
