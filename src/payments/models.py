# src/payments/models.py

import uuid
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# =================================================================
#  CHOICES
# =================================================================

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    SUCCESSFUL = 'successful', _('Successful')
    FAILED = 'failed', _('Failed')
    REFUNDED = 'refunded', _('Refunded')

# =================================================================
#  PAYMENT MODEL
# =================================================================

class Payment(models.Model):
    """
    Represents a single financial transaction.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, # In case user is deleted, we might want to keep financial records
        verbose_name=_("User")
    )
    amount = models.DecimalField(
        _("Amount"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Amount in the specified currency")
    )
    currency = models.CharField(
        _("Currency"),
        max_length=3,
        default='GBP', # Default to Gibraltar's currency
        help_text=_("Currency code (e.g., GBP, EUR)")
    )
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    
    # --- Gateway Information ---
    gateway_transaction_id = models.CharField(
        _("Gateway Transaction ID"),
        max_length=255,
        blank=True,
        db_index=True, # Indexed for fast lookups
        help_text=_("The unique ID from the payment provider (e.g., Stripe, PayPal)")
    )
    gateway_name = models.CharField(
        _("Gateway Name"),
        max_length=50,
        blank=True,
        help_text=_("e.g., 'Stripe', 'PayPal'")
    )

    # --- Timestamps ---
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Payment")
        verbose_name_plural = _("Payments")
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} for {self.amount} {self.currency} by {self.user}"