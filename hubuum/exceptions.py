"""Generic exceptions for hubuum."""

from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class MissingParam(Exception):
    """An exception thrown when a parameter is missing, or the param lacks a value."""


class Conflict(APIException):
    """Thrown when trying to overwrite an existing object."""

    status_code = status.HTTP_409_CONFLICT
    default_detail = _("Resource already exists.")
    default_code = "resource_exists"
