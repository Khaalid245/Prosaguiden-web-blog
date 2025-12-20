from django.urls import path
from .views import (
    CommentListCreateView,
    CommentDetailView,
    ToggleLikeCommentView
)

urlpatterns = [
    path('comments/', CommentListCreateView.as_view(), name='comments'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<int:pk>/like/', ToggleLikeCommentView.as_view(), name='comment-like'),
]
