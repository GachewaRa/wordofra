from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
from django.utils.text import slugify

# Model for Services
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = CloudinaryField('image', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

# Model for Projects
class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True, editable=False)
    description = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)
    link = models.URLField(max_length=300, blank=True)  # Optional link to live project or repo
    tags = models.CharField(max_length=100, blank=True)  # Comma-separated tags (e.g., 'Python, Django, API')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:  # Only generate slug if it's not set
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Project.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
