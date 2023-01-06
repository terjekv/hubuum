"""Filters for hubuum permissions."""
from rest_framework import filters
from django.apps import apps


class DjangoObjectPermissionsFilter(filters.BaseFilterBackend):
    """Return viewable objects for a user with Guardian object permissions.

    This filter returns (request.)user-visible objects of a model in question.
    """

    perm_format = "%(app_label)s.view_%(model_name)s"
    shortcut_kwargs = {
        "accept_global_perms": False,
    }

    def __init__(self):
        """Ensure that django-guardian is installed."""
        assert apps.is_installed("guardian"), (
            "Using DjangoObjectPermissionsFilter, "
            "but django-guardian is not installed."
        )

    def filter_queryset(self, request, queryset, view):
        """Perform the filtering."""
        from guardian.shortcuts import get_objects_for_user

        user = request.user
        permission = self.perm_format % {
            "app_label": queryset.model._meta.app_label,
            "model_name": queryset.model._meta.model_name,
        }

        return get_objects_for_user(user, permission, queryset, **self.shortcut_kwargs)
