# src/listings/translation.py

from modeltranslation.translator import register, TranslationOptions
from .models import Listing

@register(Listing)
class ListingTranslationOptions(TranslationOptions):
    """
    Defines which fields of the Listing model should be translated.
    """
    fields = ('title', 'description')