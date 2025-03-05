
import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status

from portfolio.models import Project, Service


@pytest.fixture
def service_data():
    """Fixture to create service test data."""
    return {
        'name': 'Web Development',
        'description': 'Custom web development services',
    }

@pytest.fixture
def project_data():
    """Fixture to create project test data."""
    return {
        'title': 'Portfolio Website',
        'description': 'Personal portfolio showcasing projects',
        'link': 'https://example.com',
        'tags': 'Django, Python, Web'
    }

@pytest.mark.django_db
class TestServiceModel:
    def test_create_service(self, service_data):
        """Test creating a service."""
        service = Service.objects.create(**service_data)
        
        assert service.name == service_data['name']
        assert service.description == service_data['description']
        assert service.created_at is not None
        assert service.updated_at is not None
        assert str(service) == service_data['name']

    def test_service_with_icon(self, service_data):
        """Test creating a service with an icon."""
        icon = SimpleUploadedFile(
            name='test_icon.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        service_data['icon'] = icon
        
        service = Service.objects.create(**service_data)
        
        assert service.icon is not None
        assert 'service_icons/' in service.icon.name

    def test_service_ordering(self, service_data):
        """Test services are ordered by name."""
        Service.objects.create(name='ZZZ Service', description='Last service')
        Service.objects.create(name='AAA Service', description='First service')
        
        services = list(Service.objects.all())
        assert services[0].name == 'AAA Service'
        assert services[1].name == 'ZZZ Service'

@pytest.mark.django_db
class TestProjectModel:
    def test_create_project(self, project_data):
        """Test creating a project."""
        project = Project.objects.create(**project_data)
        
        assert project.title == project_data['title']
        assert project.description == project_data['description']
        assert project.link == project_data['link']
        assert project.tags == project_data['tags']
        assert project.slug == 'portfolio-website'
        assert project.created_at is not None
        assert project.updated_at is not None
        assert str(project) == project_data['title']

    def test_project_slug_generation(self, project_data):
        """Test automatic slug generation."""
        project1 = Project.objects.create(**project_data)
        assert project1.slug == 'portfolio-website'
        
        # Create another project with same title
        project_data['title'] = 'Portfolio Website'
        project2 = Project.objects.create(**project_data)
        assert project2.slug == 'portfolio-website-1'

    def test_project_with_image(self, project_data):
        """Test creating a project with an image."""
        image = SimpleUploadedFile(
            name='test_project.jpg', 
            content=b'', 
            content_type='image/jpeg'
        )
        project_data['image'] = image
        
        project = Project.objects.create(**project_data)
        
        assert project.image is not None
        assert 'project_images/' in project.image.name

    def test_project_ordering(self, project_data):
        """Test projects are ordered by creation date (newest first)."""
        # Create two projects with different creation times
        project1 = Project.objects.create(**project_data)
        project_data['title'] = 'Another Project'
        project2 = Project.objects.create(**project_data)
        
        projects = list(Project.objects.all())
        assert projects[0] == project2
        assert projects[1] == project1

@pytest.mark.django_db
class TestProjectViewSet:
    def test_list_projects(self, client):
        """Test retrieving list of projects."""
        # Create some test projects
        Project.objects.create(
            title='Test Project 1', 
            description='First test project',
            tags='Django, Python'
        )
        Project.objects.create(
            title='Test Project 2', 
            description='Second test project',
            tags='React, JavaScript'
        )
        
        url = reverse('project-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check response data
        if isinstance(response.data, list):
            assert len(response.data) == 2
        elif 'results' in response.data:
            assert len(response.data['results']) == 2

    def test_project_detail(self, client):
        """Test retrieving a single project."""
        project = Project.objects.create(
            title='Detailed Project', 
            description='Project with details',
            link='https://example.com',
            tags='Testing, Django'
        )
        print("PROJECT SLUG: ", project.slug)
        url = reverse('project-detail', kwargs={'pk': project.slug})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == project.title
        assert response.data['description'] == project.description

@pytest.mark.django_db
class TestServiceViewSet:
    def test_list_services(self, client):
        """Test retrieving list of services."""
        # Create some test services
        Service.objects.create(
            name='Web Development', 
            description='Custom web development services'
        )
        Service.objects.create(
            name='Mobile App Development', 
            description='Cross-platform mobile app development'
        )
        
        url = reverse('service-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Check response data
        if isinstance(response.data, list):
            assert len(response.data) == 2
        elif 'results' in response.data:
            assert len(response.data['results']) == 2

    def test_service_detail(self, client):
        """Test retrieving a single service."""
        service = Service.objects.create(
            name='Data Analysis', 
            description='Professional data analysis services'
        )
        
        url = reverse('service-detail', kwargs={'pk': service.pk})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == service.name
        assert response.data['description'] == service.description