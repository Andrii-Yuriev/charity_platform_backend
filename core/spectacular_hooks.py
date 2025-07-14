from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import UserDetailsView


def pre_processing_hook(endpoints):
    """
    Цей хук виконує дві дії:
    1. Видаляє стандартний ендпоінт /auth/user/ від dj-rest-auth з документації.(Уникаємо дублювання)
    2. Групує решту ендпоінтів dj-rest-auth під тегом 'Authentication'.
    """

    filtered_endpoints = []
    for path, path_regex, method, callback in endpoints:
        if (
            hasattr(callback, "view_class")
            and callback.view_class is UserDetailsView
        ):
            continue

        filtered_endpoints.append((path, path_regex, method, callback))

    auth_paths = [
        "/api/v1/auth/login/",
        "/api/v1/auth/logout/",
        "/api/v1/auth/password/change/",
        "/api/v1/auth/password/reset/",
        "/api/v1/auth/password/reset/confirm/",
        "/api/v1/auth/token/verify/",
        "/api/v1/auth/token/refresh/",
    ]

    for path, path_regex, method, callback in filtered_endpoints:
        if hasattr(callback, "view_class") and path in auth_paths:
            callback.view_class = extend_schema(tags=["Authentication"])(
                callback.view_class
            )

    return filtered_endpoints
