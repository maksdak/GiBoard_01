# src/categories/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    """
    Model for hierarchical categories using django-mptt.
    """
    name = models.CharField(_("Category Name"), max_length=100, unique=True)
    slug = models.SlugField(_("Slug"), max_length=150, unique=True, help_text=_("A short, URL-friendly version of the name."))
    
    parent = TreeForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        db_index=True
    )
    
    is_active = models.BooleanField(_("Is Active"), default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name

# --- NEW MODELS FOR DYNAMIC FIELDS ---

class Field(models.Model):
    """
    A global definition of a possible field for a listing.
    e.g., "Mileage", "Square Feet", "Color".
    """
    class FieldType(models.TextChoices):
        TEXT = 'text', _('Text')
        NUMBER = 'number', _('Number')
        BOOLEAN = 'boolean', _('Yes / No')
        # We can add more types later, e.g., 'date', 'select'
        
    name = models.CharField(_("Field Name"), max_length=100, unique=True)
    field_type = models.CharField(_("Field Type"), max_length=10, choices=FieldType.choices)
    
    class Meta:
        verbose_name = _("Field Definition")
        verbose_name_plural = _("Field Definitions")
        ordering = ['name']
        
    def __str__(self):
        return f"{self.name} ({self.get_field_type_display()})"
        

class CategoryField(models.Model):
    """
    Links a Field to a Category, making it available for listings in that category.
    """
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category_fields')
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='category_fields')
    is_required = models.BooleanField(_("Is Required"), default=False)
    
    class Meta:
        verbose_name = _("Category Field")
        verbose_name_plural = _("Category Fields")
        # Ensure a field is only linked once to a category
        unique_together = ('category', 'field')

    def __str__(self):
        return f'"{self.field.name}" for category "{self.category.name}"'