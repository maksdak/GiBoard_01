# src/moderation/models.py

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

# =================================================================
#  CHOICES
# =================================================================

class ReportStatus(models.TextChoices):
    """
    Defines the status of a moderation report.
    """
    SUBMITTED = 'submitted', _('Submitted')
    UNDER_REVIEW = 'under_review', _('Under Review')
    RESOLVED_VALID = 'resolved_valid', _('Resolved (Action Taken)')
    RESOLVED_INVALID = 'resolved_invalid', _('Resolved (No Action Needed)')

# =================================================================
#  REPORT MODEL
# =================================================================

class Report(models.Model):
    """
    Represents a user-submitted report against a piece of content.
    """
    # --- Who reported it and why ---
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep the report even if the user is deleted
        null=True,
        blank=True,
        verbose_name=_("Reporter")
    )
    reason = models.TextField(
        _("Reason for Reporting"),
        help_text=_("User's explanation of why they are reporting this content.")
    )

    # --- What is being reported (Generic Relation) ---
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("Content Type")
    )
    object_id = models.PositiveIntegerField(
        _("Object ID")
    )
    content_object = GenericForeignKey('content_type', 'object_id')

    # --- Moderation Status ---
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.SUBMITTED
    )
    moderator_notes = models.TextField(
        _("Moderator Notes"),
        blank=True,
        help_text=_("Internal notes for the moderation team.")
    )
    created_at = models.DateTimeField(_("Reported At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Last Updated"), auto_now=True)

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ['-created_at']

    def __str__(self):
        return _("Report on %(content)s by %(user)s") % {
            'content': self.content_object,
            'user': self.reporter or 'Anonymous'
        }