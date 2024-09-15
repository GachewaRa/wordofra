from django.contrib import admin
from .models import Post, Category, Tag

# Registering the models
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

