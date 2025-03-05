import sys
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Category, Tag, Post, Quote, Comment

User = get_user_model()

@pytest.fixture
def api_client():
    """Fixture to create a test API client."""
    return APIClient()

@pytest.fixture
def authenticated_user(db):
    """Fixture to create and return an authenticated user."""
    user = User.objects.create_user(
        username='testuser', 
        email='test@example.com', 
        password='testpass123'
    )
    return user

@pytest.fixture
def category(db):
    """Fixture to create a test category."""
    return Category.objects.create(name='Test Category')

@pytest.fixture
def tag(db):
    """Fixture to create a test tag."""
    return Tag.objects.create(name='Test Tag')

@pytest.fixture
def post(db, authenticated_user, category):
    """Fixture to create a test post."""
    return Post.objects.create(
        title='Test Post',
        content='Test content',
        author=authenticated_user,
        category=category,
        status='published'
    )

@pytest.fixture
def quote(db):
    """Fixture to create a test quote."""
    return Quote.objects.create(
        content='Test quote content',
        owner='Test Owner'
    )

import pytest
from django.urls import reverse
from rest_framework import status

@pytest.mark.django_db
class TestCategoryViewSet:
    def test_list_categories(self, api_client, category):
        """Test retrieving list of categories."""
        url = reverse('category-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        
        # Print response to diagnose
        print("Response data:", response.data)
        
        # Check if response is a list or has a 'results' key
        if isinstance(response.data, list):
            # If it's a direct list of categories
            assert len(response.data) > 0
        elif 'results' in response.data:
            # If it uses pagination
            assert len(response.data['results']) > 0
        else:
            # If neither condition is true, fail the test
            raise AssertionError("Unexpected response format")
        
        # Optional: Additional assertions about the category
        if isinstance(response.data, list):
            assert any(cat['name'] == category.name for cat in response.data)
        else:
            assert any(cat['name'] == category.name for cat in response.data['results'])

    def test_category_detail(self, api_client, category):
        """Test retrieving a single category."""
        url = reverse('category-detail', kwargs={'pk': category.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == category.name

@pytest.mark.django_db
class TestTagViewSet:
    def test_list_tags(self, api_client, tag):
        """Test retrieving list of tags."""
        url = reverse('tag-list')
        response = api_client.get(url)
        print("Response Data: ", response.data)
        assert response.status_code == status.HTTP_200_OK
        if isinstance(response.data, dict) and 'results' in response.data:
            # Pagination is enabled
            assert len(response.data['results']) > 0
        elif isinstance(response.data, list):
            # No pagination
            assert len(response.data) > 0
        else:
            # Handle unexpected response
            pytest.fail("Unexpected response data format")

    def test_tag_detail(self, api_client, tag):
        """Test retrieving a single tag."""
        url = reverse('tag-detail', kwargs={'pk': tag.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == tag.name

@pytest.mark.django_db
class TestPostViewSet:
    def test_list_posts(self, api_client, post):
        """Test retrieving list of published posts."""
        url = reverse('post-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_retrieve_post(self, api_client, post):
        """Test retrieving a single post by slug."""
        url = reverse('post-detail', kwargs={'pk': post.slug})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == post.title

    def test_filter_posts_by_category(self, api_client, post, category):
        """Test filtering posts by category."""
        url = reverse('post-list') + f'?category={category.slug}'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_filter_posts_by_tag(self, api_client, post, tag):
        """Test filtering posts by tag."""
        post.tags.add(tag)
        url = reverse('post-list') + f'?tag={tag.slug}'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_restricted_post_access(self, api_client, authenticated_user):
        """Test access to restricted posts."""
        category = Category.objects.create(name="Test Category", slug="test-category")
        # Create a restricted post
        restricted_post = Post.objects.create(
            title='Restricted Post',
            content='Restricted content',
            author=authenticated_user,
            category=category,
            status='published',
            is_restricted=True
        )

        # Try accessing as an unauthenticated user
        url = reverse('post-detail', kwargs={'pk': restricted_post.slug})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
class TestQuoteViewSet:
    def test_list_quotes(self, api_client, quote):
        """Test retrieving list of quotes."""
        url = reverse('quote-list')
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        if isinstance(response.data, dict) and 'results' in response.data:
            # Pagination is enabled
            assert len(response.data['results']) > 0
        elif isinstance(response.data, list):
            # No pagination
            assert len(response.data) > 0
        else:
            # Handle unexpected response
            pytest.fail("Unexpected response data format")

    def test_quote_detail(self, api_client, quote):
        """Test retrieving a single quote."""
        url = reverse('quote-detail', kwargs={'pk': quote.pk})
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['content'] == quote.content

@pytest.mark.django_db
class TestCommentViewSet:
    def test_list_comments(self, api_client, post, authenticated_user):
        """Test retrieving list of comments for a post."""
        # Create an approved comment
        comment = Comment.objects.create(
            post=post, 
            user=authenticated_user, 
            content='Test comment',
            is_approved=True
        )

        url = reverse('comment-list') + f'?post={post.id}'
        response = api_client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) > 0

    def test_create_comment(self, api_client, authenticated_user, post):
        """Test creating a comment."""
        api_client.force_authenticate(user=authenticated_user)
        
        url = reverse('comment-list')
        data = {
            'post': post.id,
            'content': 'New test comment',
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'New test comment'
        assert response.data['user'] == authenticated_user.email

    def test_create_comment_unauthenticated(self, api_client, post):
        """Test comment creation fails for unauthenticated users."""
        url = reverse('comment-list')
        data = {
            'post': post.id,
            'content': 'Unauthorized comment',
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_comment_on_quote(self, api_client, authenticated_user, quote):
        """Test creating a comment on a quote."""
        api_client.force_authenticate(user=authenticated_user)
        
        url = reverse('comment-list')
        data = {
            'quote': quote.id,
            'content': 'Comment on quote',
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['content'] == 'Comment on quote'
        assert response.data['quote'] == quote.id

    def test_comment_without_post_or_quote(self, api_client, authenticated_user):
        """Test creating a comment fails without a post or quote."""
        api_client.force_authenticate(user=authenticated_user)
        
        url = reverse('comment-list')
        data = {
            'content': 'Invalid comment',
        }
        
        response = api_client.post(url, data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST