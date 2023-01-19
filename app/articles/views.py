from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .permissions import IsOwnerOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Article, Rating, Category
from .serializers import (
    ArticleSerializer,
    ArticleSerializerCreate,
    RatingSerializer,
    CategorySerializer,
)
from . import client
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from app.users.models import User
from .tasks import count_views, rate_article


class SearchListView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("q")
        classify = request.GET.get("classify")
        if not query:

            result = client.perform_search("", classify)
            return Response(result)
        result = client.perform_search(query, classify)
        return Response(result)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    permission_classes = (IsAuthenticated, IsAdminUser)


class ArticleCreateAPIView(generics.CreateAPIView):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializerCreate

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        if isinstance(self.request.user, User):
            serializer.save(author=self.request.user)


class ArticleListAPIView(generics.ListAPIView):
    queryset = Article.objects.all().order_by("-created_at")
    serializer_class = ArticleSerializer


class ArticleDetailAPIView(generics.RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        pk = obj.pk
        count_views.delay(pk)
        return self.retrieve(request, *args, **kwargs)


class ArticleUpdateAPIView(generics.UpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)

    def perform_update(self, serializer):
        return super().perform_update(serializer)


class ArticleDeleteAPIView(generics.DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "pk"
    permission_classes = [IsOwnerOrReadOnly]

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class RatingView(generics.GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk=None):
        user = request.user
        article_id = Article.objects.get(pk=pk).pk
        value = request.data.get("value")
        if value is not None:
            try:
                rating = Rating.objects.get(
                    user=user, article=article_id
                    )
            except:
                rating = None
            if rating:
                return Response(
                    {"detail": "You have already rated this article"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                rate_article.delay(int(user.pk), article_id, value)
                return Response(
                    {"detail": "the article has been rated!"},
                    status=status.HTTP_200_OK,
                )
                
        else:
            return Response(
                {"detail": "You don't enter with a value"},
                status=status.HTTP_400_BAD_REQUEST,
            )
