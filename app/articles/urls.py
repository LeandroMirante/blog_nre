from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", views.CategoryViewSet)


urlpatterns = [
    path("category/", include(router.urls)),
    path("<int:pk>/", views.ArticleDetailAPIView.as_view(), name="article-detail"),
    path(
        "<int:pk>/update/", views.ArticleUpdateAPIView.as_view(), name="article-update"
    ),
    path(
        "<int:pk>/delete/", views.ArticleDeleteAPIView.as_view(), name="article-delete"
    ),
    path("", views.ArticleListAPIView.as_view(), name="article-list"),
    path("create/", views.ArticleCreateAPIView.as_view(), name="article-create"),
    path("search/", views.SearchListView.as_view()),
    path("<int:pk>/rating/", views.RatingView.as_view(), name="article-rating"),
]
