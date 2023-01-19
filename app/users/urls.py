from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.urls import path, include
from app.users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"user", views.UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("api/register/", views.RegisterView.as_view(), name="register"),
    path("api/login/", views.LoginView.as_view(), name="login"),
]
