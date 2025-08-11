# src/locations/models.py

from django.db import models
from django.contrib.gis.db.models import PointField  # <-- 1. ADD THIS IMPORT
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    """
    Model to store countries.
    """
    name = models.CharField(_("Country Name"), max_length=100, unique=True)
    code = models.CharField(_("Country Code"), max_length=2, unique=True, help_text=_("ISO 3166-1 alpha-2 code"))

    class Meta:
        verbose_name = _("Country")
        verbose_name_plural = _("Countries")
        ordering = ['name']

    def __str__(self):
        return self.name

class City(models.Model):
    """
    Model to store cities. Linked to a country.
    For Gibraltar, we might only have one or a few entries.
    """
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="cities")
    name = models.CharField(_("City Name"), max_length=100)
    # The PointField is the core of PostGIS functionality.
    # It stores longitude and latitude.
    location = PointField(_("Location"), null=True, blank=True) # <-- 2. REMOVE "models." PREFIX

    class Meta:
        verbose_name = _("City")
        verbose_name_plural = _("Cities")
        ordering = ['name']
        # Ensure a city name is unique within a country
        unique_together = ('country', 'name')

    def __str__(self):
        return self.name