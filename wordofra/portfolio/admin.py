from django.contrib import admin

# Register your models here.

from .models import Project, Service

admin.site.register(Project)
admin.site.register(Service)
