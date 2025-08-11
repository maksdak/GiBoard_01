# src/categories/admin.py

from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from modeltranslation.admin import TabbedTranslationAdmin
from import_export.admin import ImportExportMixin

from .models import Category, Field, CategoryField

# --- Inlines ---

class CategoryFieldInline(admin.TabularInline):
    """
    Allows editing the fields associated with a category directly
    on the Category admin page.
    """
    model = CategoryField
    extra = 1
    autocomplete_fields = ['field']

# --- ModelAdmins ---

@admin.register(Field)
class FieldAdmin(ImportExportMixin, admin.ModelAdmin): # <-- Added ImportExportMixin
    """
    Admin interface for the global Field definitions.
    """
    list_display = ('name', 'field_type')
    list_filter = ('field_type',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(ImportExportMixin, DraggableMPTTAdmin, TabbedTranslationAdmin):
    """
    Admin interface for categories, combining MPTT drag-drop,
    modeltranslation tabs, and import-export functionality.
    """
    # Define search_fields for autocomplete to work
    search_fields = ('name_en', 'name_es', 'slug_en', 'slug_es')
    
    list_display = ('tree_actions', 'indented_title', 'is_active')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('name',)}
    
    # The 'name' and 'slug' fields are handled by TabbedTranslationAdmin,
    # so we don't need to list them in fieldsets explicitly.
    
    inlines = [CategoryFieldInline]

@admin.register(CategoryField)
class CategoryFieldAdmin(ImportExportMixin, admin.ModelAdmin): # <-- Added ImportExportMixin
    """
    Admin interface for the CategoryField model.
    """
    list_display = ('category', 'field', 'is_required')
    search_fields = ('category__name', 'field__name')
    list_filter = ('is_required',)
    autocomplete_fields = ['category', 'field'] # Also make category searchable