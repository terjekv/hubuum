"""Non-versioned views for hubuum."""

from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication


# Allow basic auth to the Knox login view.
class LoginView(KnoxLoginView):
    """Override Knox Authentication for logins.

    We use Knox everywhere, but we need to be able to get Knox tokens somehow.
    To achieve this, we disable Knox for the LoginView.
    https://james1345.github.io/django-rest-knox/auth/#global-usage-on-all-views
    """

    authentication_classes = [BasicAuthentication]
