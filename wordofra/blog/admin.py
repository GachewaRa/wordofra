from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Category, Tag, Quote, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created_at', 'status']
    list_filter = ['status', 'tags', 'category']
    search_fields = ['title', 'content']
    ordering = ['status', 'created_at']
    
    filter_horizontal = ('tags',)  # Enables an easier UI for selecting/removing tags



# Admin class for Tag model
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    # prepopulated_fields = {'slug': ('name',)}

# Admin class for Quote model
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('owner', 'content', 'created_at')
    search_fields = ('owner', 'content')

# Admin class for Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post_or_quote', 'created_at', 'is_approved')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'content')
    actions = ['approve_comments']

    def post_or_quote(self, obj):
        return obj.post if obj.post else obj.quote
    post_or_quote.short_description = 'Post/Quote'

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = "Approve selected comments"

# Register models with their respective admin classes
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Comment, CommentAdmin)

