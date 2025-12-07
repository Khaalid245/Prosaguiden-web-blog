from django.urls import path
from .views import (
    CategoryListCreateView,
    ArticleListCreateView,
    ArticleDetailView
)

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('articles/', ArticleListCreateView.as_view(), name='articles'),
    path('articles/<slug:slug>/', ArticleDetailView.as_view(), name='article-detail'),
]
