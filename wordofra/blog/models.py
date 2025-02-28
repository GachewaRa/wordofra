from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from accounts.models import CustomUser
from tinymce.models import HTMLField


# Category model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        # Automatically generate slug from category name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'

# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        # Automatically generate slug from tag name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

# Post model
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)
    content = HTMLField()  # Use TinyMCE for content editing
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Assume you're using the default User model
    category = models.ForeignKey(Category, related_name='posts', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_restricted = models.BooleanField(default=False)  # For posts restricted to registered users

    def save(self, *args, **kwargs):
        # Automatically generate slug from title if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Quote(models.Model):
    content = models.TextField()  # The quote content
    owner = models.CharField(max_length=255)  # The person who said the quote
    owner_image = models.ImageField(upload_to='owner_images/', blank=True, null=True)  # Optional image of the quote owner
    created_at = models.DateTimeField(auto_now_add=True)  # When the quote was added

    def __str__(self):
        return f'Quote by {self.owner}'


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, null=True)
    quote = models.ForeignKey(Quote, related_name='comments', on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'