from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from django.db.models import Count, Q, Prefetch
from .models import CustomUser
from projects.models import Project, ProjectImage
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    CurrentUserSerializer,
    CustomRegisterSerializer,
    AvatarUpdateSerializer,
    FinalPasswordResetSerializer,
)
from dj_rest_auth.utils import jwt_encode
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(
        summary="Отримати список авторів",
        description="Повертає список авторів, у яких є хоча б один активний проєкт.",
        tags=["Authors"],
    ),
    retrieve=extend_schema(
        summary="Отримати публічний профіль автора", tags=["Authors"]
    ),
)
class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for view public author profile.
    - list: show only authors with active projects.
    - retrieve: show any author.
    """

    serializer_class = AuthorDetailSerializer

    def get_queryset(self):
        queryset = CustomUser.objects.annotate(
            project_count=Count(
                "projects", filter=Q(projects__status=Project.Status.ACTIVE)
            )
        )

        if self.action == "retrieve":
            queryset = queryset.prefetch_related(
                "specialization",
                Prefetch(
                    "projects",
                    queryset=Project.objects.filter(
                        status=Project.Status.ACTIVE
                    ).prefetch_related(
                        Prefetch(
                            "images",
                            queryset=ProjectImage.objects.order_by("order"),
                            to_attr="prefetched_images",
                        )
                    ),
                    to_attr="prefetched_projects",
                ),
            )
        else:
            queryset = queryset.filter(project_count__gt=0).prefetch_related(
                "specialization"
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return super().get_serializer_class()


@extend_schema(
    summary="Отримати свій профіль",
    description="Повертає дані поточного аутентифікованого користувача.",
    tags=["Profile"],
)
class CurrentUserView(generics.RetrieveAPIView):
    """
    View for retrieving the current user's profile.
    Allow on endpoint: /api/v1/users/me/
    """

    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    summary="Оновити текстові дані свого профілю",
    description="Дозволяє оновити текстові поля профілю. Надсилайте дані у форматі application/json.",
    tags=["Profile"],
)
class CurrentUserUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


@extend_schema(
    summary="Вхід через Google",
    description="""
Приймає `access_token`, отриманий від Google на стороні клієнта. 
Надсилайте запит у форматі application/json: `{\"access_token\": \"...\"}`.
У відповідь повертає JWT токени вашого додатку.
    """,
    tags=["Authentication"],
)
class GoogleLogin(SocialLoginView):
    """
    View for Google OAuth2 login.
    Allow on endpoint: /api/v1/auth/google/
    Uses acces from frontend to authenticate users via Google.
    """

    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client


@extend_schema(
    summary="Реєстрація нового користувача",
    description="Створює нового користувача за email та паролем. Повертає JWT токени.",
    tags=["Authentication"],
)
class CustomRegisterView(generics.CreateAPIView):
    serializer_class = CustomRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        access_token, refresh_token = jwt_encode(user)

        data = {
            "user": self.get_serializer(user).data,
            "access": str(access_token),
            "refresh": str(refresh_token),
        }

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(
    summary="Оновити свій аватар",
    description="""
Оновлює аватар поточного користувача. 
Надсилайте запит у форматі **multipart/form-data** з файлом у полі `avatar`.
    """,
    tags=["Profile"],
)
class AvatarUpdateView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = AvatarUpdateSerializer

    def get_object(self):
        return self.request.user


class CustomPasswordResetView(generics.GenericAPIView):
    serializer_class = FinalPasswordResetSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"detail": "Лист для скидання паролю надіслано."},
            status=status.HTTP_200_OK,
        )
