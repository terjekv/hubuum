"""Filters for hubuum permissions."""
from rest_framework import filters

from hubuum.models import Permissions


class DjangoObjectPermissionsFilter(filters.BaseFilterBackend):
    """Return viewable objects for a user.

    This filter returns (request.)user-visible objects of a model in question.
    """

    def filter_queryset(self, request, queryset, view):
        """Perform the filtering."""
        user = request.user
        # model = queryset.model._meta.model_name
        #        permission = self.perm_format % {
        #            "app_label": queryset.model._meta.app_label,
        #            "model_name": queryset.model._meta.model_name,
        #        }

        #    Find all namespaces we can perform the given operation in.

        #        print("List of {}".format(model))
        res = Permissions.objects.filter(has_read=True, group__in=user.groups.all())
        if not res:
            return []

        return queryset.filter(namespace__in=res.namespace)


#        return get_objects_for_user(user, permission, queryset, **self.shortcut_kwargs)
