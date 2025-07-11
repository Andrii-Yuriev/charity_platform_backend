from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AuthorViewSet, CurrentUserView

router = DefaultRouter()
router.register(r"authors", AuthorViewSet, basename="author")

urlpatterns = [
    # path("me/", CurrentUserView.as_view(), name="current-user"),
    path("", include(router.urls)),
]
