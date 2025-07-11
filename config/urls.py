from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from users.views import GoogleLogin, CustomRegisterView
from users.views import CurrentUserView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/projects", include("projects.urls")),
    path("api/v1/users", include("users.urls")),
    path("api/v1/me/", CurrentUserView.as_view(), name="current-user"),
    # Authentication URLs
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path(
        "api/v1/auth/registration/",
        CustomRegisterView.as_view(),
        name="custom_register",
    ),
    # Google Login URL
    path("api/v1/auth/google/", GoogleLogin.as_view(), name="google_login"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
