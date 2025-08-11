# src/places/models.py

from django.db import models
from django.contrib.gis.db.models import PointField
from django.utils.translation import gettext_lazy as _

# =================================================================
#  PLACE CATEGORY MODEL
# =================================================================

class PlaceCategory(models.Model):
    """
    A category for classifying places, e.g., 'Restaurant', 'Museum', 'Viewpoint'.
    """
    name = models.CharField(
        _("Name"),
        max_length=100
    )
    slug = models.SlugField(
        _("Slug"),
        unique=True,
        help_text=_("A unique, URL-friendly version of the name.")
    )
    icon = models.CharField(
        _("Icon"),
        max_length=50,
        blank=True,
        help_text=_("Optional: Icon identifier, e.g., from Font Awesome like 'fa-utensils'.")
    )

    class Meta:
        verbose_name = _("Place Category")
        verbose_name_plural = _("Place Categories")
        ordering = ['name']

    def __str__(self):
        return self.name

# =================================================================
#  PLACE MODEL
# =================================================================

class Place(models.Model):
    """
    Represents a specific place of interest in Gibraltar.
    """
    name = models.CharField(
        _("Name"),
        max_length=255
    )
    category = models.ForeignKey(
        PlaceCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='places',
        verbose_name=_("Category")
    )
    description = models.TextField(
        _("Description"),
        blank=True
    )
    address = models.CharField(
        _("Address"),
        max_length=255,
        blank=True
    )
    location = PointField(
        _("Geographic Location"),
        null=True,
        blank=True,
        help_text=_("The precise point on the map. Click to set.")
    )
    image = models.ImageField(
        _("Image"),
        upload_to='places/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text=_("A featured image for the place.")
    )
    is_approved = models.BooleanField(
        _("Is Approved"),
        default=True,
        help_text=_("Uncheck this to hide the place from the main site.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Place")
        verbose_name_plural = _("Places")
        ordering = ['name']

    def __str__(self):
        return self.name