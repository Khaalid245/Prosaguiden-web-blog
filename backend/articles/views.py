from rest_framework import generics, permissions
from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from .permissions import IsAdminOrWriter, IsOwnerOrAdmin

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAdminUser]


class ArticleListCreateView(generics.ListCreateAPIView):
    queryset = Article.objects.filter(status="published")
    serializer_class = ArticleSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrWriter()]
        return []


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]
        return []
