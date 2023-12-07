"""
URL mappings for the user API.
"""
from django.urls import path

from user import views


# Used in reverse function syntax Eg. (user:create)
app_name = 'user'

# .as_view() is used on the Class because Django expects
# actual functions in the urlpatterns and the default
# as_view() function provided by the rest_framework
# converts the class to a usable view function.

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
]
