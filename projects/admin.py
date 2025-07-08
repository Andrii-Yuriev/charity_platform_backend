from django.contrib import admin
from .models import Category, Project, ProjectImage


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    fields = ("image", "order")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]
    list_display = (
        "title",
        "author",
        "status",
        "category",
        "created_at",
        "end_date",
    )
    list_filter = ("status", "category", "donation_type")
    search_fields = ("title", "author__username", "description")
    readonly_fields = ("created_at", "updated_at", "views_count")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
