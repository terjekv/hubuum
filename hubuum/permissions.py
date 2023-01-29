"""Permissions module for hubuum."""
from rest_framework.permissions import (
    SAFE_METHODS,
    DjangoObjectPermissions,
    IsAuthenticated,
)


class CustomObjectPermissions(DjangoObjectPermissions):
    """Map permissions towards CRUD."""

    perms_map = {
        "GET": ["%(app_label)s.read_%(model_name)s"],
        "OPTIONS": ["%(app_label)s.read_%(model_name)s"],
        "HEAD": ["%(app_label)s.read_%(model_name)s"],
        "POST": ["%(app_label)s.create_%(model_name)s"],
        "PUT": ["%(app_label)s.update_%(model_name)s"],
        "PATCH": ["%(app_label)s.update_%(model_name)s"],
        "DELETE": ["%(app_label)s.delete_%(model_name)s"],
    }


def operation_exists(permission):
    """Check if a permission label is valid."""
    return permission in ("create", "read", "update", "delete", "namespace")


def is_super_or_admin(user):
    """Check to see if a user is superuser or admin (staff)."""
    return user.is_staff or user.is_superuser


class IsAuthenticatedAndReadOnly(IsAuthenticated):
    """Allow read-only access if authenticated."""

    def has_permission(self, request, view):
        """Check super (IsAuthenticated) and read-only methods (SAFE_METHODS)."""
        if not super().has_permission(request, view):
            return False
        return request.method in SAFE_METHODS


class IsSuperOrAdminOrReadOnly(IsAuthenticatedAndReadOnly):
    """Permit super or admin users, else read only."""

    def has_permission(self, request, view):
        """Check if we're super/admin otherwise authenticated readonly."""
        if is_super_or_admin(request.user):
            return True
        return super().has_permission(request, view)


# A thing here. Everyone can read all namespaces. For multi-tenant installations we probably need:
# 1. Tenant specific admin groups
# 2. Limit visibility to a tenant's namespace / scope.
class NameSpaceOrReadOnly(IsSuperOrAdminOrReadOnly):
    """
    Namespace access.

    Write access:
        - super or admin users
        - users with has_namespace for the namespace set

    Read access:
        - Everyone logged in
    """

    def has_permission(self, request, view):
        """Check if R/O or admin by delegation, then check user, otherwise false."""
        if super().has_permission(request, view):
            return True

        return request.user.can_modify_namespaces(request.data["name"])
