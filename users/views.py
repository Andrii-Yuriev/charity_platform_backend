from rest_framework import viewsets, permissions, generics
from django.db.models import Count, Q
from .models import CustomUser
from projects.models import Project
from .serializers import (
    AuthorListSerializer,
    AuthorDetailSerializer,
    CurrentUserSerializer,
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
        ).prefetch_related("specialization")

        if self.action == "list":
            return queryset.filter(project_count__gt=0)

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return (
            super().get_serializer_class()
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
