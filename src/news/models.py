# src/news/models.py

from django.db import models
from django.utils.translation import gettext_lazy as _

class NewsArticle(models.Model):
    title = models.CharField(_("Title"), max_length=200)
    content = models.TextField(_("Content"), blank=True)
    published_at = models.DateTimeField(_("Published At"), auto_now_add=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("News Article")
        verbose_name_plural = _("News Articles")
        ordering = ['-published_at']

    def __str__(self):
        return self.title