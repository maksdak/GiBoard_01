# src/notifications/models.py

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

# =================================================================
#  NOTIFICATION MODEL
# =================================================================

class Notification(models.Model):
    """
    Represents a notification for a user.
    """
    # --- Who the notification is for ---
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name=_("Recipient")
    )

    # --- Notification Content ---
    message = models.TextField(
        _("Message"),
        help_text=_("The content of the notification to be displayed to the user.")
    )
    is_read = models.BooleanField(
        _("Is Read"),
        default=False,
        db_index=True # Index for faster filtering of unread notifications
    )

    # --- Optional link to a related object ---
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_("Related Content Type")
    )
    object_id = models.PositiveIntegerField(
        _("Related Object ID"),
        null=True,
        blank=True
    )
    related_object = GenericForeignKey('content_type', 'object_id')

    # --- Timestamps ---
    created_at = models.DateTimeField(
        _("Created At"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("Notification")
        verbose_name_plural = _("Notifications")
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.get_username()}: {self.message[:40]}..."