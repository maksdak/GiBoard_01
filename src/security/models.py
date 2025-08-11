# src/security/models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# =================================================================
#  CHOICES
# =================================================================

class ActivityType(models.TextChoices):
    LOGIN_SUCCESS = 'login_success', _('Successful Login')
    LOGIN_FAILED = 'login_failed', _('Failed Login Attempt')
    LOGOUT = 'logout', _('Logout')
    PASSWORD_RESET_REQUEST = 'pw_reset_request', _('Password Reset Request')
    PASSWORD_RESET_SUCCESS = 'pw_reset_success', _('Password Reset Successful')
    LISTING_CREATED = 'listing_created', _('Listing Created')
    LISTING_DELETED = 'listing_deleted', _('Listing Deleted')

# =================================================================
#  USER ACTIVITY LOG MODEL
# =================================================================

class UserActivityLog(models.Model):
    """
    Logs significant actions performed by users for security and auditing.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True, # Allows logging actions for anonymous users (e.g., failed login)
        verbose_name=_("User")
    )
    action = models.CharField(
        _("Action"),
        max_length=20,
        choices=ActivityType.choices,
        help_text=_("The type of action performed.")
    )
    ip_address = models.GenericIPAddressField(
        _("IP Address"),
        null=True,
        blank=True,
        help_text=_("The IP address of the user when the action was performed.")
    )
    details = models.TextField(
        _("Details"),
        blank=True,
        help_text=_("Any additional details about the action, e.g., user agent or object ID.")
    )
    timestamp = models.DateTimeField(
        _("Timestamp"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("User Activity Log")
        verbose_name_plural = _("User Activity Logs")
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.get_username() if self.user else "Anonymous"
        return f"{user_str} - {self.get_action_display()} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"