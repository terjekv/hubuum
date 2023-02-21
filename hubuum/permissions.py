"""Permissions module for hubuum."""
# from rest_framework.exceptions import ValidationError
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


def operations():
    """Define the list of valid operations."""
    return ("create", "read", "update", "delete", "namespace")


def fully_qualified_operations():
    """Define the list of valid operations, fully qualified with the has_-prefix."""
    return ["has_" + s for s in operations()]


def operation_exists(permission, fully_qualified=False):
    """Check if a permission label is valid."""
    if fully_qualified:
        return permission in fully_qualified_operations()
    else:
        return permission in operations()


def is_super_or_admin(user):
    """Check to see if a user is superuser or admin (staff)."""
    return user.is_staff or user.is_superuser


class IsSuperOrAdmin(IsAuthenticated):
    """Permit super or admin users."""

    def has_permission(self, request, view):
        """Check if we're super/admin otherwise false."""
        if is_super_or_admin(request.user):
            return True

        return False

    def has_object_permission(self, request, view, obj):
        """Check if we're super/admin otherwise false."""
        if is_super_or_admin(request.user):
            return True

        return False


class IsAuthenticatedAndReadOnly(IsAuthenticated):
    """Allow read-only access if authenticated."""

    def has_permission(self, request, view):
        """Check super (IsAuthenticated) and read-only methods (SAFE_METHODS)."""
        if not super().has_permission(request, view):
            return False
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        """Check super (IsAuthenticated) and read-only methods (SAFE_METHODS)."""
        if not super().has_object_permission(request, view, obj):
            return False
        return request.method in SAFE_METHODS


class IsSuperOrAdminOrReadOnly(IsAuthenticatedAndReadOnly):
    """Permit super or admin users, else read only."""

    def has_permission(self, request, view):
        """Check if we're super/admin otherwise authenticated readonly."""
        if is_super_or_admin(request.user):
            return True
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """Check if we're super/admin otherwise authenticated readonly."""
        if is_super_or_admin(request.user):
            return True
        return super().has_object_permission(request, view, obj)


# A thing here. Everyone can read all namespaces. For multi-tenant installations we probably need:
# 1. Tenant specific admin groups
# 2. Limit visibility to a tenant's namespace / scope.
class NameSpace(IsSuperOrAdminOrReadOnly):
    """
    Namespace access.

    Write access:
        - super or admin users
        - users in groups with has_namespace for the namespace set

    Read access:
        - super or admin users
        - users in groups with has_read for the namespace set
    """

    def has_permission(self, request, view):
        """Check if superuser or admin by delegation, then check user, otherwise false."""
        # First check if we are superuser or asking for read-only (listing), if so, return true.
        if super().has_permission(request, view):
            return True

        # POST needs special treatment as we don't have an object to work on.
        # The lack of an object means we can't delegate to has_object_permission, as it will
        # never get called...
        # Instead we have to check for has_create or has_namespace depending on context.
        # For now though, users can't create anything...
        # The question here is how we find the primary key that is being created so
        # we can pass that to can_modify_namespace()...
        if request.method == "POST":
            return False
        #            return request.user.can_modify_namespace()

        return True

    def has_object_permission(self, request, view, obj):
        """Check for object-specific access."""
        # We can't user the super method, as it allows read-only for everyone,
        # which we don't want.
        if is_super_or_admin(request.user):
            return True

        perms_map = {
            "GET": "has_read",
            "OPTIONS": "has_read",
            "HEAD": "has_read",
            "POST": "has_create",
            "PUT": "has_update",
            "PATCH": "has_update",
            "DELETE": "has_delete",
        }

        return request.user.namespaced_can(perms_map[request.method], obj)
