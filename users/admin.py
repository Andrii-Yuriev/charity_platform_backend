from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    ordering = ("email",)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password", "password2"),
            },
        ),
    )

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            return (
                (None, {"fields": ("email",)}),
                (
                    "Персональна інформація",
                    {
                        "fields": (
                            "first_name",
                            "last_name",
                            "username",
                            "bio",
                            "city",
                            "avatar_original",
                        )
                    },
                ),
                (
                    "Контакти",
                    {
                        "fields": (
                            "phone_number",
                            "telegram_url",
                            "instagram_url",
                            "facebook_url",
                        )
                    },
                ),
                ("Спеціалізація", {"fields": ("specialization",)}),
                (
                    "Права доступу",
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "is_superuser",
                            "groups",
                        )
                    },
                ),
                ("Важливі дати", {"fields": ("last_login", "date_joined")}),
            )
        else:
            return (
                (
                    "Персональна інформація",
                    {
                        "fields": (
                            "first_name",
                            "last_name",
                            "bio",
                            "city",
                            "avatar_original",
                        )
                    },
                ),
                (
                    "Контакти",
                    {
                        "fields": (
                            "phone_number",
                            "telegram_url",
                            "instagram_url",
                            "facebook_url",
                        )
                    },
                ),
                ("Спеціалізація", {"fields": ("specialization",)}),
            )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)
