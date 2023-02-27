"""Tools for huubum."""

from django.contrib.auth.models import Group
from rest_framework.exceptions import NotFound

from hubuum.models import Namespace, Permission, User


def get_user(user_identifier, raise_exception=True):
    """Try to find a user based on the identifier.

    Searches in User.lookup_fields
    """
    return get_object(User, user_identifier, raise_exception=raise_exception)


def get_group(group_identifier, raise_exception=True):
    """Try to find a group based on the identifier.

    param: group_identifier

    return: group object

    raises: NotFound if no object found.
    """
    return get_object(
        Group,
        group_identifier,
        lookup_fields=["id", "name"],
        raise_exception=raise_exception,
    )


def get_permission(namespace: Namespace, group: Group, raise_exception=True):
    """Try to find a permission object for the (namespace, group) touple.

    param: namespace (Namespace instance)
    param: group (Group instance)

    returns: permission object

    raises: NotFound if no object found.
    """
    try:
        obj = Permission.objects.get(namespace=namespace, group=group)
        return obj
    except Permission.DoesNotExist as exc:
        if raise_exception:
            raise NotFound() from exc
        return None


def get_object(cls, lookup_value, lookup_fields=None, raise_exception=True):
    """Get a object from a class.

    A generic way to find objects in a model.
    By default the list of fields searched are in order of precedence:
      - the list passed to the lookup_fields keyword argument
      - the models class attribute 'lookup_fields'
      - the list ["id"]

    param: cls (the model to look into)
    param: lookup_value (value to search for)
    param: lookup_fields=[] (explicitly declare fields to look into)

    return object or None
    """
    obj = None
    fields = ["id"]
    if lookup_fields:
        fields = lookup_fields
    elif hasattr(cls, "lookup_fields"):
        fields = cls.lookup_fields

    for field in fields:
        try:
            obj = cls.objects.get(**{field: lookup_value})
            if obj:
                return obj

        except Exception:  # nosec pylint: disable=broad-except
            pass

    if raise_exception:
        raise NotFound()

    return None
