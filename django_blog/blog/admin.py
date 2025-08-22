from django.contrib import admin
from .models import Post, Comment, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Post model.
    """
    list_display = ('title', 'author', 'published_date', 'tag_list')
    list_filter = ('published_date', 'author', 'tags')
    search_fields = ('title', 'content', 'tags__name')
    ordering = ('-published_date',)
    date_hierarchy = 'published_date'
    filter_horizontal = ('tags',)
    
    def tag_list(self, obj):
        """Return a comma-separated list of tags."""
        return ", ".join([tag.name for tag in obj.tags.all()])
    tag_list.short_description = 'Tags'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Comment model.
    """
    list_display = ('author', 'post', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'author', 'post')
    search_fields = ('content', 'author__username', 'post__title')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Tag model.
    """
    list_display = ('name', 'created_at', 'post_count')
    list_filter = ('created_at',)
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('created_at',)
    
    def post_count(self, obj):
        """Return the number of posts using this tag."""
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'
