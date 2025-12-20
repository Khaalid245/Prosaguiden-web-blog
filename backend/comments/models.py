from django.db import models
from django.conf import settings
from articles.models import Article

User = settings.AUTH_USER_MODEL


class Comment(models.Model):
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField()

    # Facebook-style replies
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )

    # 👍 Likes
    likes = models.ManyToManyField(
        User,
        related_name='liked_comments',
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        return f'Comment by {self.author}'
