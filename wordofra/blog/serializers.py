from rest_framework import serializers
from blog.models import Category, Comment, Post, Quote, Tag

class PostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', read_only=True)
    tags = serializers.SlugRelatedField(slug_field='slug', read_only=True, many=True)
    author = serializers.StringRelatedField()  # Returns author's name instead of ID

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'image', 'author', 'category', 'tags', 
            'created_at', 'updated_at', 'status', 'is_restricted'
        ]
        

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  # Show username instead of ID
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), required=False, allow_null=True)
    quote = serializers.PrimaryKeyRelatedField(queryset=Quote.objects.all(), required=False, allow_null=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'quote', 'user', 'content', 'created_at', 'is_approved']

    def validate(self, data):
        """
        Ensure that a comment is linked to either a Post or a Quote but not both.
        """
        if not data.get('post') and not data.get('quote'):
            raise serializers.ValidationError("A comment must be linked to either a Post or a Quote.")
        return data



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

    

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ['id', 'content', 'owner', 'owner_image', 'created_at']

