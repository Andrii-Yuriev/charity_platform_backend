from django.core.management.base import BaseCommand
from django.utils import timezone
from projects.models import Project
from datetime import timedelta


class Command(BaseCommand):
    help = "Archives active projects that are 30 days or older."

    def handle(self, *args, **options):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        projects_to_archive = Project.objects.filter(
            status=Project.Status.ACTIVE, created_at__lte=thirty_days_ago
        )

        count = projects_to_archive.count()

        if count > 0:
            updated_count = projects_to_archive.update(
                status=Project.Status.ARCHIVED
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully archived {updated_count} project(s) older than 30 days."
                )
            )
        else:
            self.stdout.write(
                self.style.NOTICE(
                    "No active projects older than 30 days to archive."
                )
            )
