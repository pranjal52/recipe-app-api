"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""
    ordering = ['id']
    list_display = ['email', 'name']

    fieldsets = (
        # Section 1 on the change page doesn't have a section header
        (None, {'fields': ('email', 'password')}),

        # Section 2 on the change page doesn't has a
        # section header "Personal Info" and shows
        # the name field. By using the django translation's
        # gettext_lazy method, we ensure that the header
        # text get's translated into any supported language
        # but is only translated whenever the actual text is
        #  needed (translated value not stored anywhere)

        (_('Personal Info'), {'fields': ('name',)}),

        # Section 2 on the change page doesn't has a
        # section header "Permissions"
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),

        # Section 2 on the change page doesn't has a
        # section header "Important Dates"
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

    add_fieldsets = (
        (None, {
            # CSS classes that can be used to modify the admin appearance
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


# Extra parameter UserAdmin is passed to ensure it uses the above
# UserAdmin and ot the default one.
admin.site.register(models.User, UserAdmin)
