from portfolio.models import Project, Service
from portfolio.serializers import ProjectSerializer, ServiceSerializer
from rest_framework import viewsets, permissions

# Create your views here.
# Portfolio App Viewsets
class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.AllowAny]

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [permissions.AllowAny]