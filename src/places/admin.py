# src/places/admin.py

from django.contrib.gis import admin
from modeltranslation.admin import TabbedTranslationAdmin
from .models import PlaceCategory, Place

# =================================================================
#  PLACE CATEGORY ADMIN
# =================================================================

@admin.register(PlaceCategory)
class PlaceCategoryAdmin(TabbedTranslationAdmin):
    """
    Admin configuration for PlaceCategory model with translation tabs.
    """
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

# =================================================================
#  PLACE ADMIN
# =================================================================

@admin.register(Place)
class PlaceAdmin(TabbedTranslationAdmin, admin.GISModelAdmin):
    """
    Admin configuration for Place model.
    - Inherits from TabbedTranslationAdmin for EN/ES fields.
    - Inherits from GISModelAdmin to get a map widget for the 'location' field.
    """
    list_display = ('name', 'category', 'address', 'is_approved', 'updated_at')
    list_filter = ('is_approved', 'category', 'updated_at')
    search_fields = ('name', 'description', 'address')

    # Note: GISModelAdmin provides the map widget automatically.
    # In some older versions of Django/PostGIS, you might need to specify:
    # gis_widget = admin.OSMWidget
    # But it's usually not necessary with modern versions.