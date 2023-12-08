"""
Views for the recipe APIs
"""

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import (
    viewsets,
    mixins,
    status,
)
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import (
    Recipe,
    Tag,
    Ingredient
)
from recipe import serializers


# ModelViewSet has a lot of pre-defined logic to work with
# models for CRUD ops
class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer

    # Objects available for this ViewSet (all recipes)
    queryset = Recipe.objects.all()

    # Defines auth method for the API
    authentication_classes = [TokenAuthentication]

    # Checks for authenticated users to be able to use
    # the API
    permission_classes = [IsAuthenticated]

    # Overiding the get_queryset method so that only available
    # recipes to manage throught the APIs are the
    # ones created by the current user
    def get_queryset(self):
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-id')

    # Override the get_serializer_class function to use the RecipeSerializer
    # class is the action is list but in all other cases use the
    # RecipeDetailSerializer class
    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return serializers.RecipeSerializer
        elif self.action == 'upload_image':
            return serializers.RecipeImageSerializer

        return self.serializer_class

    # Override the perform_create function
    # Everytime you create a new recipe through this ViewSet
    # Call this method after the validated data
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Mixin is a reusable code that adds extra functionality to a class
# Here the mixin adds the listing capability to the class
class TagViewSet(mixins.DestroyModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')


class IngredientViewSet(mixins.DestroyModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by('-name')
