from drf_spectacular.utils import extend_schema
from dj_rest_auth.views import UserDetailsView


def pre_processing_hook(endpoints):
    """
    Цей хук виконує три дії:
    1. Видаляє стандартний ендпоінт /auth/user/ від dj-rest-auth з документації.
    2. Групує решту ендпоінтів dj-rest-auth під тегом 'Authentication'.
    3. Додає кастомні описи для деяких з цих ендпоінтів.
    """

    path_descriptions = {
        "/api/v1/auth/logout/": extend_schema(
            summary="Вихід з системи",
            description="Анулює refresh токен, додаючи його до чорного списку. Потрібно передати `refresh_token` в тілі запиту.",
        ),
        "/api/v1/auth/login/": extend_schema(
            summary="Вхід в систему (Email)",
            description="Приймає `email` та `password`, у відповідь повертає JWT токени.",
        ),
        "/api/v1/auth/token/refresh/": extend_schema(
            summary="Оновлення access токену",
            description="Приймає `refresh_token`, у відповідь повертає новий `access_token`.",
        ),
    }

    auth_paths = [
        "/api/v1/auth/login/",
        "/api/v1/auth/logout/",
        "/api/v1/auth/password/change/",
        "/api/v1/auth/password/reset/",
        "/api/v1/auth/password/reset/confirm/",
        "/api/v1/auth/token/verify/",
        "/api/v1/auth/token/refresh/",
    ]

    processed_endpoints = []

    for path, path_regex, method, callback in endpoints:

        if (
            hasattr(callback, "view_class")
            and callback.view_class is UserDetailsView
        ):
            continue

        if hasattr(callback, "view_class"):
            if path in auth_paths:
                callback.view_class = extend_schema(tags=["Authentication"])(
                    callback.view_class
                )

            if path in path_descriptions:
                callback.view_class = path_descriptions[path](
                    callback.view_class
                )

        processed_endpoints.append((path, path_regex, method, callback))

    return processed_endpoints
