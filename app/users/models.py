from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .managers import LowercaseEmailField, CustomUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class User(AbstractBaseUser, PermissionsMixin):
    email = LowercaseEmailField(_("email address"), unique=True)
    name = models.CharField(max_length=255)
    profile_picture = models.ImageField(upload_to="files", null=True, blank=True)
    is_staff = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone = models.CharField(blank=True, unique=False, max_length=255)
    birth_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text=_("Ativo ou inativo"),
        verbose_name=_("Status"),
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        return super().save(*args, **kwargs)

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
