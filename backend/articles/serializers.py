from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ArticleSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'cover_image', 'status', 'author', 'author_username',
            'category', 'created_at', 'updated_at', 'published_at'
        ]
        read_only_fields = [
            'slug', 'author', 'created_at',
            'updated_at', 'published_at'
        ]
