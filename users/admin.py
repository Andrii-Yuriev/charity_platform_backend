from django.contrib import admin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ("email", "first_name", "last_name", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email",),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (
                    "Персональна інформація",
                    {
                        "fields": (
                            "first_name",
                            "last_name",
                            "email",
                            "avatar_original",
                        )
                    },
                ),
                (
                    "Права доступу",
                    {"fields": ("is_active", "is_staff", "is_superuser")},
                ),
                ("Важливі дати", {"fields": ("last_login", "date_joined")}),
            )
        else:
            return (
                (
                    "Персональна інформація",
                    {"fields": ("first_name", "last_name", "avatar_original")},
                ),
            )

    def get_form(self, request, obj=None, **kwargs):
        if not obj:
            return self.add_form
        return super().get_form(request, obj, **kwargs)

    def add_view(self, request, form_url="", extra_context=None):
        self.fieldsets = self.add_fieldsets
        return super().add_view(request, form_url, extra_context)
