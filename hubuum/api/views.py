from knox.views import LoginView as KnoxLoginView
from rest_framework.authentication import BasicAuthentication

# Allow basic auth to the Knox login view.
class LoginView(KnoxLoginView):
    authentication_classes = [BasicAuthentication]
