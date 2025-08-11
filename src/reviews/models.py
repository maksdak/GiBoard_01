# src/reviews/models.py

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _ # <-- THIS LINE WAS MISSING
from listings.models import Listing

class Review(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(_("Review Text"))
    rating = models.PositiveSmallIntegerField(_("Rating"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Review")
        verbose_name_plural = _("Reviews")
        ordering = ['-created_at']
        unique_together = ('listing', 'author')

    def __str__(self):
        return f"Review by {self.author} for {self.listing.title}"