from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsCommentOwner


class CommentPagination(PageNumberPagination):
    page_size = 10


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    pagination_class = CommentPagination

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        article_id = self.request.query_params.get('article')
        return Comment.objects.filter(
            article_id=article_id,
            parent__isnull=True
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsCommentOwner]


class ToggleLikeCommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        comment = Comment.objects.get(pk=pk)

        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            return Response({"liked": False})
        else:
            comment.likes.add(request.user)
            return Response({"liked": True})
