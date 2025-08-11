# src/listings/models.py

import uuid
from django.conf import settings
from django.db import models
from django.utils.text import slugify # <-- ADD THIS IMPORT
from django.utils.translation import gettext_lazy as _

# Import related models from other apps
from categories.models import Category, CategoryField
from locations.models import City


# --- Helper function moved to the top level of the module ---
def get_listing_image_path(instance, filename):
    """
    Generates a unique path for each uploaded image.
    `instance` is the ListingImage instance being saved.
    e.g., listings/images/<listing_public_id>/<filename>
    """
    return f'listings/images/{instance.listing.public_id}/{filename}'


class Listing(models.Model):
    # ... (all fields remain the same)
    class SaleType(models.TextChoices):
        FOR_SALE = 'for_sale', _('For Sale')
        FOR_RENT = 'for_rent', _('For Rent')
        EXCHANGE = 'exchange', _('Exchange')
    
    class Condition(models.TextChoices):
        NEW = 'new', _('New')
        USED = 'used', _('Used')
        NOT_APPLICABLE = 'na', _('Not Applicable')

    # Core Fields
    title = models.CharField(_("Title"), max_length=200)
    slug = models.SlugField(_("Slug"), max_length=255, unique=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='listings')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='listings')
    
    # Pricing and Sale Type
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    currency = models.CharField(_("Currency"), max_length=3, default='GBP', choices=[('GBP', 'GBP'), ('EUR', 'EUR')])
    sale_type = models.CharField(_("Sale Type"), max_length=10, choices=SaleType.choices, default=SaleType.FOR_SALE)
    
    # Details
    condition = models.CharField(_("Condition"), max_length=10, choices=Condition.choices, default=Condition.USED)
    
    # Status and Timestamps
    is_active = models.BooleanField(_("Is Active"), default=True, help_text=_("Is the listing visible to users?"))
    is_sold = models.BooleanField(_("Is Sold"), default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    
    # A unique public ID to avoid exposing the primary key in URLs
    public_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    
    # --- Overridden Methods ---
    
    def save(self, *args, **kwargs):
        """
        Overrides the save method to automatically generate the slug if it's empty.
        """
        if not self.slug:
            # Create a base slug from the title
            base_slug = slugify(self.title)
            # To ensure uniqueness, append the public_id
            # This is a simple and robust way to prevent slug collisions.
            self.slug = f"{base_slug}-{str(self.public_id)[:8]}"
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("Listing")
        verbose_name_plural = _("Listings")
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ... (ListingImage and ListingFieldValue classes remain unchanged)
class ListingImage(models.Model):
    """
    An image associated with a listing.
    A listing can have multiple images.
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(_("Image"), upload_to=get_listing_image_path)
    alt_text = models.CharField(
        _("Alt Text"), 
        max_length=255, 
        blank=True, 
        help_text=_("A short description of the image for accessibility and SEO.")
    )
    order = models.PositiveIntegerField(_("Order"), default=0, help_text=_("Order in which images are displayed."))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Listing Image")
        verbose_name_plural = _("Listing Images")
        ordering = ['order']

    def __str__(self):
        return f"Image for {self.listing.title} (Order: {self.order})"

class ListingFieldValue(models.Model):
    """
    Stores the actual value for a dynamic field for a specific listing.
    e.g., Listing "Toyota Corolla" -> Field "Mileage" -> Value "150000"
    """
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='field_values')
    field = models.ForeignKey(CategoryField, on_delete=models.CASCADE, related_name='listing_values')
    value = models.CharField(_("Value"), max_length=500)
    
    class Meta:
        verbose_name = _("Listing Field Value")
        verbose_name_plural = _("Listing Field Values")
        # A listing should only have one value for a specific field
        unique_together = ('listing', 'field')
        
    def __str__(self):
        return f'{self.listing.title} - {self.field.field.name}: {self.value}'