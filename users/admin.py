from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "email",
        "username",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("email", "username", "first_name", "last_name")

    def get_fieldsets(self, request, obj=None):
        # Якщо це супер-адмін, показуємо йому ВСЕ
        if request.user.is_superuser:
            return (
                (None, {"fields": ("email", "password")}),
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
                (
                    "Права доступу",
                    {
                        "fields": (
                            "is_active",
                            "is_staff",
                            "is_superuser",
                            "groups",
                            "user_permissions",
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

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(pk=request.user.pk)

    def add_view(self, request, form_url="", extra_context=None):
        if request.method == "POST":
            form = self.get_form(request)(request.POST, request.FILES)
            if not form.is_valid():
                print("--- ADMIN VALIDATION ERRORS ---")
                print(form.errors.as_json())
                print("-----------------------------")
        return super().add_view(request, form_url, extra_context)
