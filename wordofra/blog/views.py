# Create your views here.
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response 
from rest_framework import viewsets, filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework import viewsets, permissions
from .models import Post, Category, Tag, Comment, Quote
from .serializers import (
    PostSerializer, CategorySerializer, TagSerializer,
    CommentSerializer, QuoteSerializer,
)

# Blog App Viewsets

class PostPagination(PageNumberPagination):
    page_size = 10  # Default number of posts per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for listing and retrieving blog posts.
    """
    serializer_class = PostSerializer
    permission_classes = [AllowAny]
    pagination_class = PostPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Default ordering (newest first)

    def get_queryset(self):
        """
        Custom queryset filtering based on query parameters.
        """
        queryset = Post.objects.filter(status='published')

        # Filtering by category
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Filtering by tag
        tag_slug = self.request.query_params.get('tag', None)
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # Filtering by author
        author_id = self.request.query_params.get('author', None)
        if author_id:
            queryset = queryset.filter(author_id=author_id)

        # Handling restricted posts
        if self.request.user.is_authenticated:
            # Authenticated users can see all posts
            return queryset
        else:
            # Public users can only see unrestricted posts
            return queryset.filter(is_restricted=False)

    def retrieve(self, request, *args, **kwargs):
        """
        Fetch a single post by slug instead of ID.
        """
        slug = kwargs.get('pk')  # Django REST uses 'pk' by default
        post = get_object_or_404(Post, slug=slug, status='published')

        if post.is_restricted and not request.user.is_authenticated:
            return Response({"detail": "This post is restricted. Please log in."}, status=403)

        serializer = self.get_serializer(post)
        return Response(serializer.data)



class CommentPagination(PageNumberPagination):
    page_size = 10  # Default comments per page
    page_size_query_param = 'page_size'
    max_page_size = 50

class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for listing, retrieving, creating, and managing comments.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = CommentPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']  # Show newest comments first

    def get_queryset(self):
        """
        Custom filtering for comments based on post, quote, or user.
        """
        queryset = Comment.objects.filter(is_approved=True)  # Only show approved comments by default

        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)

        quote_id = self.request.query_params.get('quote', None)
        if quote_id:
            queryset = queryset.filter(quote_id=quote_id)

        user_id = self.request.query_params.get('user', None)
        if user_id:
            queryset = queryset.filter(user_id=user_id)

        return queryset

    def perform_create(self, serializer):
        """
        Ensure a user is assigned when creating a comment.
        """
        serializer.save(user=self.request.user)



class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny]

class QuoteViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Quote.objects.all().order_by('-created_at')
    serializer_class = QuoteSerializer
    permission_classes = [permissions.AllowAny]


