# src/content/translation.py

from modeltranslation.translator import register, TranslationOptions
from .models import StaticPage

# =================================================================
#  STATIC PAGE TRANSLATIONS
# =================================================================

@register(StaticPage)
class StaticPageTranslationOptions(TranslationOptions):
    """
    Translation options for the StaticPage model.
    """
    fields = ('title', 'content')