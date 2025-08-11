# src/news/admin.py

from django.contrib import admin
from .models import NewsArticle  # Import our model

# Register the model with the admin site to make it visible and editable
@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    # Fields to display in the news articles list
    list_display = ('title', 'published_at', 'is_active')

    # Filters in the right sidebar
    list_filter = ('is_active', 'published_at')

    # Fields to be used for searching
    search_fields = ('title', 'content')