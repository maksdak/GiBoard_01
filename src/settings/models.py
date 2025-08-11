# src/settings/models.py

from django.db import models
from solo.models import SingletonModel
from django.utils.translation import gettext_lazy as _

# =================================================================
#  SITE SETTINGS MODEL (SINGLETON)
# =================================================================

class SiteSettings(SingletonModel):
    """
    A singleton model to store global site settings, editable in the admin panel.
    There will only ever be one instance of this model.
    """
    # --- General Settings ---
    site_name = models.CharField(
        _("Site Name"),
        max_length=100,
        default="GiBoard"
    )
    contact_email = models.EmailField(
        _("Public Contact Email"),
        max_length=255,
        blank=True
    )

    # --- Social Media Links ---
    facebook_url = models.URLField(
        _("Facebook URL"),
        blank=True
    )
    twitter_url = models.URLField(
        _("Twitter URL"),
        blank=True
    )
    instagram_url = models.URLField(
        _("Instagram URL"),
        blank=True
    )

    # --- Maintenance Mode ---
    maintenance_mode = models.BooleanField(
        _("Maintenance Mode"),
        default=False,
        help_text=_(
            "If checked, a maintenance page will be shown to all non-staff users."
        )
    )

    class Meta:
        verbose_name = _("Site Settings")
        verbose_name_plural = _("Site Settings")

    def __str__(self):
        # The __str__ method MUST return a concrete string, not a lazy proxy.
        return "Site Settings" # <--- THIS IS THE FIX