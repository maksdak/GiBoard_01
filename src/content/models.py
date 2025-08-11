# src/content/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# =================================================================
#  STATIC PAGE MODEL
# =================================================================

class StaticPage(models.Model):
    """
    Represents a static page on the site, e.g., 'About Us' or 'Privacy Policy'.
    """
    title = models.CharField(
        _("Title"),
        max_length=200
    )
    slug = models.SlugField(
        _("URL Slug"),
        unique=True,
        help_text=_("A unique, URL-friendly version of the title. E.g., 'about-us'")
    )
    content = models.TextField(
        _("Content"),
        blank=True,
        help_text=_("The main content of the page, can use HTML.")
    )
    is_published = models.BooleanField(
        _("Is Published"),
        default=False,
        help_text=_("Check this to make the page visible on the site.")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Static Page")
        verbose_name_plural = _("Static Pages")
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # This will be useful later for creating sitemaps or linking to pages
        return reverse('static_page_detail', args=[self.slug])