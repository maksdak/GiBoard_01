# src/advertising/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

# =================================================================
#  BANNER MODEL
# =================================================================

class Banner(models.Model):
    """
    Represents a single advertising banner.
    """
    name = models.CharField(
        _("Banner Name"),
        max_length=255,
        help_text=_("Internal name for this banner, e.g., 'Homepage Top Banner'")
    )
    image = models.ImageField(
        _("Image"),
        upload_to='banners/%Y/%m/%d/',
        help_text=_("The actual banner image file.")
    )
    url = models.URLField(
        _("URL Link"),
        max_length=2000,
        blank=True,
        null=True,
        help_text=_("The destination URL when the banner is clicked. Can be empty.")
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Uncheck this to hide the banner from the site without deleting it.")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Banner")
        verbose_name_plural = _("Banners")
        ordering = ['-created_at']

    def __str__(self):
        return self.name