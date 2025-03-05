from django.urls import path, include
from rest_framework.routers import DefaultRouter
from portfolio.views import ProjectViewSet, ServiceViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
]
