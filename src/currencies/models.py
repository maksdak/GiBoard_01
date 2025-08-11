from django.db import models

# Create your models here.
# src/currencies/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

class CurrencyRate(models.Model):
    source_currency = models.CharField(_("Source Currency"), max_length=3, default='GBP')
    target_currency = models.CharField(_("Target Currency"), max_length=3, default='EUR')
    rate = models.DecimalField(_("Rate"), max_digits=15, decimal_places=6)
    last_updated = models.DateTimeField(_("Last Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Currency Rate")
        verbose_name_plural = _("Currency Rates")
        unique_together = ('source_currency', 'target_currency')

    def __str__(self):
        return f"1 {self.source_currency} = {self.rate} {self.target_currency}"