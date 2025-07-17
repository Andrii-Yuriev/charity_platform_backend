from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from users.views import (
    GoogleLogin,
    CustomRegisterView,
    CurrentUserView,
    CurrentUserUpdateView,
    AvatarUpdateView,
)

urlpatterns = [
    # Admin URL
    path("admin/", admin.site.urls),
    # Apps
    path("api/v1/projects/", include("projects.urls")),
    path("api/v1/users/", include("users.urls")),
    # Authentication URLs
    path(
        "api/v1/auth/user/", CurrentUserView.as_view(), name="rest_user_details"
    ),
    path(
        "api/v1/auth/user/",
        CurrentUserView.as_view(),
        name="rest_user_details_read",
    ),
    path(
        "api/v1/auth/user/update/",
        CurrentUserUpdateView.as_view(),
        name="rest_user_details_update",
    ),
    path(
        "api/v1/auth/user/avatar/",
        AvatarUpdateView.as_view(),
        name="rest_user_avatar_update",
    ),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path(
        "api/v1/auth/registration/",
        CustomRegisterView.as_view(),
        name="custom_register",
    ),
    # Google Login URL
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
    # API
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI:
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc:
    path(
        "api/v1/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
