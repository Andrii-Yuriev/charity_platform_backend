from rest_framework import viewsets, permissions, generics, status
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import CustomUser
from projects.models import Project
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    CurrentUserSerializer,
    CustomRegisterSerializer,
)
from dj_rest_auth.utils import jwt_encode
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView


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
        ).prefetch_related("specialization")

        if self.action == "list":
            return queryset.filter(project_count__gt=0)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return super().get_serializer_class()


class CurrentUserView(generics.RetrieveAPIView):
    """
    View for retrieving the current user's profile.
    Allow on endpoint: /api/v1/users/me/
    """

    serializer_class = CurrentUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class GoogleLogin(SocialLoginView):
    """
    View for Google OAuth2 login.
    Allow on endpoint: /api/v1/auth/google/
    Uses acces from frontend to authenticate users via Google.
    """

    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:3000"
    client_class = OAuth2Client


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
