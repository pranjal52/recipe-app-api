"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


# A validation class that handles validating and
# storing the JSON data to a model.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:

        # Validation logic to be stored in this class
        model = get_user_model()

        # Fields that are mandatory
        fields = ['email', 'password', 'name']

        # Other fields
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""

        # We override the original create method of the serializer
        # because the below method from core.models handles
        # password encryption.

        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""

        # We need to serialize the password before storing
        # Hence we pop it out of the received validated data
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            # And set the password using set_password here
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    # Defining the serializer with 2 fields
    email = serializers.EmailField()

    # Style is input_type as password because with browsable
    # APIs it should be of the hidden(****) type
    # Also, the whitespaces will not be trimmed in password field
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        # This method will be triggered when someone POSTs on the view

        # Getting the fields from the view attributes
        email = attrs.get('email')
        password = attrs.get('password')

        # Using the built in authenticate function of django
        # request is a required field
        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
