import re
from rest_framework import serializers
from blog.models import Category, Comment, Post, Quote, Tag


class PostListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for post list views - excludes full content."""
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    tags = serializers.SlugRelatedField(slug_field="slug", read_only=True, many=True)
    author = serializers.StringRelatedField()
    excerpt = serializers.SerializerMethodField()
    first_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "image", "author", "category", "tags",
            "created_at", "updated_at", "status", "is_restricted",
            "excerpt", "first_image_url"
        ]

    def get_excerpt(self, obj):
        text = re.sub(r"<[^>]+>", "", obj.content)
        text = text.strip()
        return text[:150] + "..." if len(text) > 150 else text

    def get_first_image_url(self, obj):
        pattern = r'''<img[^>]+src=["']([^"'>]+)["']'''
        match = re.search(pattern, obj.content)
        if match:
            src = match.group(1)
            if not src.startswith("data:"):
                return src
        return None


class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    tags = serializers.SlugRelatedField(slug_field="slug", read_only=True, many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "content", "image", "author", "category", "tags",
            "created_at", "updated_at", "status", "is_restricted"
        ]


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True)
    quote = serializers.PrimaryKeyRelatedField(queryset=Quote.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ["id", "post", "quote", "user", "content", "created_at", "is_approved"]

    def validate(self, data):
        if not data.get("post") and not data.get("quote"):
            raise serializers.ValidationError("A comment must be linked to either a Post or a Quote.")
        return data


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ["id", "content", "owner", "owner_image", "created_at"]
