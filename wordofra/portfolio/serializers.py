from rest_framework import serializers
from portfolio.models import Project, Service

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'title', 'slug', 'description', 'image', 'link', 'tags', 'created_at', 'updated_at']



class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['id', 'name', 'description', 'icon', 'created_at', 'updated_at']
