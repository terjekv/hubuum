from rest_framework import filters
from django.conf import settings

class DjangoObjectPermissionsFilter(filters.BaseFilterBackend):
    perm_format = '%(app_label)s.view_%(model_name)s'
    shortcut_kwargs = {
        'accept_global_perms': False,
    }

    def __init__(self):
        assert 'guardian' in settings.INSTALLED_APPS, (
            'Using DjangoObjectPermissionsFilter, '
            'but django-guardian is not installed.')

    def filter_queryset(self, request, queryset, view):
        from guardian.shortcuts import get_objects_for_user

        user = request.user
        permission = self.perm_format % {
            'app_label': queryset.model._meta.app_label,
            'model_name': queryset.model._meta.model_name,
        }

        return get_objects_for_user(
            user, permission, queryset,
            **self.shortcut_kwargs)