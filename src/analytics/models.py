# src/analytics/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.conf import settings # We can add this later for User relation

# =================================================================
#  PAGE VIEW MODEL
# =================================================================

class PageView(models.Model):
    """
    Represents a single view of a page.
    A very basic model for now, to be expanded later.
    """
    url_path = models.CharField(
        _("URL Path"),
        max_length=2000,
        help_text=_("The path of the page visited, e.g., '/listings/my-awesome-item/'")
    )
    # user = models.ForeignKey(
    #     settings.AUTH_USER_MODEL,
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     verbose_name=_("User")
    # ) # Commented out for now to keep it simple
    timestamp = models.DateTimeField(
        _("Timestamp"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Page View")
        verbose_name_plural = _("Page Views")
        ordering = ['-timestamp']

    def __str__(self):
        return f"View of {self.url_path} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"