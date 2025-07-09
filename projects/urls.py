from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProjectViewSet

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"projects", ProjectViewSet, basename="project")

urlpatterns = router.urls
