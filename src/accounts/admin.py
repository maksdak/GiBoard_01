# src/accounts/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    """
    Defines the admin interface configuration for the CustomUser model.
    """
    # We add our custom fields to the admin display.
    # The 'fieldsets' attribute controls the layout of the edit form.
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Profile', {
            'fields': ('avatar', 'public_id')
        }),
    )
    
    # 'add_fieldsets' controls the layout of the "add user" form.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Profile', {
            'fields': ('avatar',) # public_id is generated automatically
        }),
    )

    # Define which fields to show in the list view of users.
    list_display = (
        'email', 
        'username', 
        'first_name', 
        'last_name', 
        'is_staff',
        'get_public_id_short' # Our custom field
    )
    
    # Define which fields are read-only in the edit form.
    readonly_fields = ('public_id',)

    # Define which fields can be used for searching.
    search_fields = ('email', 'username')
    
    # Define the default ordering.
    ordering = ('email',)
    
    @admin.display(description='Public ID')
    def get_public_id_short(self, obj):
        """
        Displays a shortened version of the UUID in the list view.
        """
        return str(obj.public_id).split('-')[0]

# Register the CustomUser model with our custom admin class.
admin.site.register(CustomUser, CustomUserAdmin)