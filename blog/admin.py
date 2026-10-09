from django.contrib import admin

from .models import Author, Category, Comment, Post, Profile, Tag


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "published", "published_at")
    list_filter = ("published", "category")
    search_fields = ("title",)


admin.site.register([Author, Profile, Category, Tag, Comment])
