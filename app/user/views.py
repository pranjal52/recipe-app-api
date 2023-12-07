"""
Views for the user API.
"""

# Generics has support for basic rest operations like
# create, read, update and delete which can be implemented
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)


# Basing it from CreateAPIView inherits the properties
# of a post request to create an object.
# By basing from this, we have to do nothing,
# but define the serialixer class and it will get
# the model name, validation and every logic from
# the serializer class.
class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""

    # generic.CreateAPIView is a default view provided by
    # rest_framework to handle POST Create calls.
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""

    # ObtainAuthToken is provided by rest_framework by default
    serializer_class = AuthTokenSerializer

    # Optional but ensures that the token API is available
    # in the docs.
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""

    # This generic class RetrieveUpdateAPIView handles update
    serializer_class = UserSerializer

    # THe auth class set previously
    authentication_classes = [authentication.TokenAuthentication]

    # The only permission required for a user to access the
    # API is that they must be authenticated.
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user
