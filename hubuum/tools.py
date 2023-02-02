"""Tools for huubum."""

from django.contrib.auth.models import Group

from hubuum.models import User


def get_user(user_identifier):
    """Tries to find a user based on the identifier.

    Searches in User.lookup_fields
    """
    return get_object(User, user_identifier)


def get_group(group_identifier):
    """Tries to find a group based on the identifier.

    param: group_identifier

    return: group object or None
    """

    return get_object(Group, group_identifier, lookup_fields=["id", "name"])


def get_object(cls, lookup_value, lookup_fields=None):
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

    return None
