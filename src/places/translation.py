# src/places/translation.py

from modeltranslation.translator import register, TranslationOptions
from .models import PlaceCategory, Place

# =================================================================
#  PLACE CATEGORY TRANSLATIONS
# =================================================================

@register(PlaceCategory)
class PlaceCategoryTranslationOptions(TranslationOptions):
    """
    Translation options for the PlaceCategory model.
    """
    fields = ('name',)
    # The 'slug' is usually not translated to maintain a consistent URL.

# =================================================================
#  PLACE TRANSLATIONS
# =================================================================

@register(Place)
class PlaceTranslationOptions(TranslationOptions):
    """
    Translation options for the Place model.
    """
    fields = ('name', 'description', 'address')