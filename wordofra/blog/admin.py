from django.contrib import admin
from .models import Post, Category, Tag

# Registering the models
#admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)


from django import forms
from tinymce.widgets import TinyMCE

# Custom form to use CKEditor for content field
class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))

    class Meta:
        model = Post
        fields = '__all__'

# Admin class to use the custom form
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm

# Register Post model with custom admin
admin.site.register(Post, PostAdmin)
