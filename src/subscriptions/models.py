# src/subscriptions/models.py

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime

# =================================================================
#  PLAN MODEL
# =================================================================

class Plan(models.Model):
    """
    Defines a subscription plan/tier.
    """
    name = models.CharField(
        _("Plan Name"),
        max_length=100,
        unique=True,
        help_text=_("e.g., 'Basic', 'Premium', 'Business'")
    )
    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("A short description of the plan's features.")
    )
    price = models.DecimalField(
        _("Price"),
        max_digits=10,
        decimal_places=2,
        help_text=_("Price per subscription period (e.g., monthly).")
    )
    duration_days = models.PositiveIntegerField(
        _("Duration (in days)"),
        default=30,
        help_text=_("The length of one subscription period.")
    )
    is_active = models.BooleanField(
        _("Is Active"),
        default=True,
        help_text=_("Uncheck to prevent new subscriptions to this plan.")
    )

    class Meta:
        verbose_name = _("Plan")
        verbose_name_plural = _("Plans")
        ordering = ['price']

    def __str__(self):
        return self.name

# =================================================================
#  SUBSCRIPTION MODEL
# =================================================================

class Subscription(models.Model):
    """
    Links a user to a subscription plan.
    """
    class SubscriptionStatus(models.TextChoices):
        ACTIVE = 'active', _('Active')
        EXPIRED = 'expired', _('Expired')
        CANCELLED = 'cancelled', _('Cancelled')

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='subscription', # user.subscription
        verbose_name=_("User")
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL, # Keep subscription record even if plan is deleted
        null=True,
        verbose_name=_("Plan")
    )
    start_date = models.DateTimeField(
        _("Start Date"),
        default=timezone.now
    )
    end_date = models.DateTimeField(
        _("End Date")
    )
    status = models.CharField(
        _("Status"),
        max_length=10,
        choices=SubscriptionStatus.choices,
        default=SubscriptionStatus.ACTIVE
    )

    class Meta:
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def __str__(self):
        return f"{self.user.get_username()}'s subscription to {self.plan.name}"

    def save(self, *args, **kwargs):
        # Automatically set the end_date when creating a new subscription
        if not self.pk and self.plan: # Only on creation and if plan is set
            self.end_date = self.start_date + datetime.timedelta(days=self.plan.duration_days)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        """
        Property to check if the subscription is currently active.
        """
        return self.status == self.SubscriptionStatus.ACTIVE and self.end_date > timezone.now()