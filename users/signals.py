from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import CustomUser
from projects.models import Project, Category, ProjectImage


@receiver(post_save, sender=CustomUser)
def assign_author_permissions(sender, instance, created, **kwargs):
    if created and not instance.is_superuser:

        author_group, _ = Group.objects.get_or_create(name="Authors")

        project_content_type = ContentType.objects.get_for_model(Project)
        category_content_type = ContentType.objects.get_for_model(Category)
        user_content_type = ContentType.objects.get_for_model(CustomUser)
        project_image_content_type = ContentType.objects.get_for_model(
            ProjectImage
        )

        permissions_to_add = [
            Permission.objects.get(
                codename="add_project", content_type=project_content_type
            ),
            Permission.objects.get(
                codename="change_project", content_type=project_content_type
            ),
            Permission.objects.get(
                codename="delete_project", content_type=project_content_type
            ),
            Permission.objects.get(
                codename="view_project", content_type=project_content_type
            ),
            Permission.objects.get(
                codename="view_category", content_type=category_content_type
            ),
            Permission.objects.get(
                codename="change_customuser", content_type=user_content_type
            ),
            Permission.objects.get(
                codename="view_customuser", content_type=user_content_type
            ),
            Permission.objects.get(
                codename="add_projectimage",
                content_type=project_image_content_type,
            ),
            Permission.objects.get(
                codename="change_projectimage",
                content_type=project_image_content_type,
            ),
            Permission.objects.get(
                codename="delete_projectimage",
                content_type=project_image_content_type,
            ),
            Permission.objects.get(
                codename="view_projectimage",
                content_type=project_image_content_type,
            ),
        ]

        author_group.permissions.set(permissions_to_add)

        instance.groups.add(author_group)
