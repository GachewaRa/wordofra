from django.shortcuts import get_object_or_404
from portfolio.models import Project, Service
from portfolio.serializers import ProjectSerializer, ServiceSerializer
from rest_framework import viewsets, permissions
from rest_framework.response import Response 

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        Fetch a single project by slug instead of ID.
        """
        slug = kwargs.get('pk')  # DRF defaults to 'pk'
        project = get_object_or_404(Project, slug=slug)

        serializer = self.get_serializer(project)
        return Response(serializer.data)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]