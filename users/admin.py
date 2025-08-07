from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    list_display = ("email", "username", "first_name", "last_name", "is_staff")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def add_view(self, request, form_url="", extra_context=None):
        if self.has_add_permission(request):
            self.form = CustomUserCreationForm
            self.fieldsets = (
                (
                    None,
                    {
                        "classes": ("wide",),
                        "fields": ("email",),
                    },
                ),
            )
        return super().add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url="", extra_context=None):
        self.form = CustomUserChangeForm
        self.fieldsets = self.get_fieldsets(request)
        return super().change_view(request, object_id, form_url, extra_context)

    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return (
                (None, {"fields": ("email", "password")}),
                (
                    "Персональна інформація",
                    {
                        "fields": (
                            "first_name",
                            "last_name",
                            "username",
                            "bio",
                            "city",
                            "avatar",
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
                            "avatar",
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
