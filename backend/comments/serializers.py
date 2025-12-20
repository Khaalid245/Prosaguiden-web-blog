from rest_framework import serializers
from .models import Comment


class RecursiveReplySerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'author_username',
            'content',
            'likes_count',
            'created_at'
        ]


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.ReadOnlyField(source='author.username')
    replies = RecursiveReplySerializer(many=True, read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'article',
            'author',
            'author_username',
            'content',
            'parent',
            'replies',
            'likes_count',
            'is_liked',
            'created_at'
        ]
        read_only_fields = ['author']

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False
