"""Core URLs for the hubuum project, site configuration."""

from django.contrib import admin
from django.urls import include, path
from rest_framework.permissions import AllowAny
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(
    title="hubuum API",
    permission_classes=(AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("hubuum.api.v1.urls")),
    path("api/", include("hubuum.api.urls")),
    path("docs/", schema_view),
]
