# src/listings/admin.py

from django.contrib import admin
from modeltranslation.admin import TabbedTranslationAdmin
from import_export.admin import ImportExportMixin

from .models import Listing, ListingImage, ListingFieldValue

# --- Inlines ---

class ListingImageInline(admin.TabularInline):
    """
    Allows editing ListingImage models directly on the Listing admin page.
    """
    model = ListingImage
    extra = 1
    fields = ('image', 'alt_text', 'order')

class ListingFieldValueInline(admin.TabularInline):
    """
    Allows editing custom field values directly on the Listing admin page.
    """
    model = ListingFieldValue
    extra = 1
    autocomplete_fields = ['field']

# --- ModelAdmins ---

@admin.register(Listing)
class ListingAdmin(ImportExportMixin, TabbedTranslationAdmin):
    """
    Admin interface for Listings, combining modeltranslation tabs
    and import-export functionality.
    """
    list_display = ('title', 'author', 'category', 'city', 'price', 'currency', 'is_active', 'is_sold', 'created_at')
    list_filter = ('category', 'city', 'is_active', 'is_sold', 'currency', 'sale_type', 'condition')
    search_fields = ('title', 'description', 'author__username', 'author__email')
    
    # We no longer need prepopulated_fields for 'slug' because our model's save() method handles it.
    # We also don't need to specify translated fields like 'title' and 'description' in fieldsets.
    
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    raw_id_fields = ('author', 'category', 'city')
    
    # Add both inline model admins to this view
    inlines = [
        ListingFieldValueInline,
        ListingImageInline,
    ]

# We can also register the other models to make them exportable if needed
@admin.register(ListingImage)
class ListingImageAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('listing', 'alt_text', 'order')

@admin.register(ListingFieldValue)
class ListingFieldValueAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('listing', 'field', 'value')
    autocomplete_fields = ['listing', 'field']