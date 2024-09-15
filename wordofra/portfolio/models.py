from django.db import models

# Create your models here.
from django.utils.text import slugify

# Model for Services
class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='service_icons/', blank=True, null=True)  # Optional icon for each service
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
    image = models.ImageField(upload_to='project_images/', blank=True, null=True)  # Optional image for each project
    link = models.URLField(max_length=300, blank=True)  # Optional link to live project or repo
    tags = models.CharField(max_length=100, blank=True)  # Comma-separated tags (e.g., 'Python, Django, API')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Auto-generate slug from title
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
