from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from .models import Post, Category, Tag, Quote, Comment

# Custom form to use TinyMCE for content field
# class PostAdminForm(forms.ModelForm):
#     content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
#     slug = forms.CharField(required=False)  # Add this line

#     class Meta:
#         model = Post
#         fields = '__all__'  


# # Admin class for Post model
# class PostAdmin(admin.ModelAdmin):
#     form = PostAdminForm
#     list_display = ('title', 'author', 'status', 'created_at')
#     list_filter = ('status', 'category', 'tags')
#     search_fields = ('title', 'content')
#     prepopulated_fields = {'slug': ('title',)}  # Auto-generate slug from title
#     readonly_fields = ('slug',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created_at', 'status']
    list_filter = ['status', 'tags', 'category']
    search_fields = ['title', 'content']
    # prepopulated_fields = {'slug': ('title',)}
    # raw_id_fields = ['author']
    # date_hierarchy = 'publish'
    ordering = ['status', 'created_at']

# Admin class for Category model
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     search_fields = ('name',)
#     prepopulated_fields = {'slug': ('name',)}

# Admin class for Tag model
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

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
# admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Tag, TagAdmin)
admin.site.register(Quote, QuoteAdmin)
admin.site.register(Comment, CommentAdmin)
# admin.site.register(Post)
