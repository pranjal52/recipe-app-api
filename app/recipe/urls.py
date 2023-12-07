"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

# Router is used to automatically fetch all end points defined
# in the class (here recipes class) and register it in the
# urlpatterns.
router = DefaultRouter()

# 'recipes' is used to add the app name
router.register('recipes', views.RecipeViewSet)
router.register('tags', views.TagViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
