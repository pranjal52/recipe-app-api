"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


# Manager to have functions for User Model creation/deletion etc.
class UserManager(BaseUserManager):
    """Manager for users."""

    # Email and password args are explicitly defined but all extra
    # fields are accepted as **extra_fields. This allow the
    # create_user method to always be flexible for accepting new or
    # non-optional fields.
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""

        if not email:
            raise ValueError("User must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)

        # For encryption of password
        user.set_password(password)

        # user.save() also works but adding the parameter is
        # best practice and comes in handy if the project
        # develops multiple databases
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Assigning the UserManager to the User model
    objects = UserManager()

    # Defining the default username field as the email field
    # Django provides auth only on the username field
    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    """Recipe object."""

    # settings.AUTH_USER_MODEL references the user model
    # and doesn't need to be changed if the user mode is changed
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)

    # Text field can have multiple lines of text
    description = models.TextField(blank=True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    link = models.CharField(max_length=255, blank=True)
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    """Tag for filtering recipes."""
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
