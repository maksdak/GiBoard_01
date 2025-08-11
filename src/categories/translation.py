# src/categories/translation.py

from modeltranslation.translator import register, TranslationOptions
from .models import Category

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    """
    Defines which fields of the Category model should be translated.
    """
    fields = ('name', 'slug')