from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title="hubuum API")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("hubuum.api.v1.urls")),
    path("", include("hubuum.api.urls")),
    path("docs/", schema_view),
]
