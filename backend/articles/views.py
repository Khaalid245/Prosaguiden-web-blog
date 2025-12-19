from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Article, Category
from .serializers import ArticleSerializer, CategorySerializer
from .permissions import IsAdminOrWriter, IsOwnerOrAdmin


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrWriter]


class ArticleListCreateView(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer

    def get_queryset(self):
        return Article.objects.filter(status="published")

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminOrWriter()]
        return [AllowAny()]


class ArticleDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ArticleSerializer
    authentication_classes = [JWTAuthentication]
    lookup_field = "slug"   # ✅ IMPORTANT LINE

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role == "admin":
            return Article.objects.all()
        return Article.objects.filter(status="published")

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsOwnerOrAdmin()]
        return [AllowAny()]
