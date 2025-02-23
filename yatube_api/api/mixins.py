from rest_framework.permissions import SAFE_METHODS, AllowAny, IsAuthenticated
from .permissions import IsAuthorOrReadOnly


class DynamicPermissionMixin:
    """
    Миксин для динамического выбора набора разрешений.
    Если флаг enforce_auth_for_safe_methods равен True,\
    даже безопасные методы требуют аутентификации.
    """
    enforce_auth_for_safe_methods = False

    def get_permissions(self):
        if self.enforce_auth_for_safe_methods:
            return [IsAuthenticated(), IsAuthorOrReadOnly()]
        if self.request.method in SAFE_METHODS:
            return [AllowAny()]
        return [IsAuthenticated(), IsAuthorOrReadOnly()]
