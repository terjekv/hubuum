from django.urls import re_path
from knox import views as knox_views

from . import views

urlpatterns = [
    re_path(r"api/auth/login/", views.LoginView.as_view(), name="knox_login"),
    re_path(r"api/auth/logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    re_path(
        r"api/auth/logoutall/",
        knox_views.LogoutAllView.as_view(),
        name="knox_logoutall",
    ),
]
