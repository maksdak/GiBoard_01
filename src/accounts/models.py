# src/accounts/models.py

import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


def get_avatar_path(instance, filename):
    """
    Generates a unique path for each uploaded avatar.
    e.g., accounts/avatars/<user_uuid>/<filename>
    """
    # We use a unique ID for the user to avoid exposing username/pk
    return f'accounts/avatars/{instance.public_id}/{filename}'


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    This model is set as the default user model for the project.
    We can add more profile fields here in the future.
    """
    # --- New Fields ---
    public_id = models.UUIDField(
        default=uuid.uuid4, # <-- Return the default
        editable=False,
        unique=True,        # <-- Return unique constraint
        help_text=_("A public identifier for the user, used in URLs and file paths.")
    )
    avatar = models.ImageField(
        _("Avatar"),
        upload_to=get_avatar_path,
        null=True,
        blank=True
    )
    # We make first_name and last_name not required by default
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    
    # --- Overridden Fields ---
    email = models.EmailField(
        _("email address"),
        unique=True, # Emails must be unique
        help_text=_("Required. Please provide a unique email address."),
    )

    # --- Authentication Setup ---
    # We make USERNAME_FIELD = 'email' to use email for login.
    # By default, AbstractUser uses 'username'.
    USERNAME_FIELD = "email"
    # 'username' is still required for createsuperuser command and compatibility
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email