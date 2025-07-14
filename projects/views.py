from rest_framework import viewsets, permissions
from .models import Category, Project, ProjectImage
from django.db.models import Prefetch
from .serializers import (
    CategorySerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
)
from drf_spectacular.utils import (
    extend_schema,
    OpenApiParameter,
    extend_schema_view,
)


@extend_schema_view(
    list=extend_schema(
        summary="Отримати список категорій", tags=["Categories"]
    ),
    retrieve=extend_schema(
        summary="Отримати деталі категорії", tags=["Categories"]
    ),
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all().order_by("name")
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a project to edit it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


@extend_schema_view(
    list=extend_schema(
        summary="Отримати список активних проєктів",
        description="Повертає список проєктів зі статусом 'active'. Можна фільтрувати за ID категорії.",
        parameters=[
            OpenApiParameter(
                name="category",
                description="Фільтрувати за ID категорії",
                type=int,
            ),
        ],
        tags=["Projects"],
    ),
    retrieve=extend_schema(
        summary="Отримати деталі проєкту", tags=["Projects"]
    ),
    create=extend_schema(
        summary="Створити новий проєкт",
        description="Створює проєкт, який одразу стає активним. Потрібна аутентифікація.",
        tags=["Projects"],
    ),
    update=extend_schema(summary="Повністю оновити проєкт", tags=["Projects"]),
    partial_update=extend_schema(
        summary="Частково оновити проєкт", tags=["Projects"]
    ),
    destroy=extend_schema(summary="Видалити проєкт", tags=["Projects"]),
)
class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet for projects.
    - list: list of projects (only active projects)
    - retrieve: detail view of a project
    - create, update, delete: only for project owners
    """

    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    ]

    def get_queryset(self):
        queryset = Project.objects.filter(status=Project.Status.ACTIVE)
        return queryset.prefetch_related("author", "category").prefetch_related(
            Prefetch("images", queryset=ProjectImage.objects.order_by("order"))
        )

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectListSerializer
        return ProjectDetailSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
