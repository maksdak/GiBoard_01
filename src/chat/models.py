# src/chat/models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

# =================================================================
#  CONVERSATION MODEL
# =================================================================

class Conversation(models.Model):
    """
    Represents a conversation thread between two or more users.
    """
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='conversations',
        verbose_name=_("Participants")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Conversation")
        verbose_name_plural = _("Conversations")
        ordering = ['-updated_at']

    def __str__(self):
        return f"Conversation between {', '.join([user.get_username() for user in self.participants.all()])}"

# =================================================================
#  MESSAGE MODEL
# =================================================================

class Message(models.Model):
    """
    Represents a single message within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_("Conversation")
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, # Keep message even if sender's account is deleted
        null=True,
        verbose_name=_("Sender")
    )
    content = models.TextField(_("Content"))
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(_("Is Read"), default=False)

    class Meta:
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        ordering = ['timestamp']

    def __str__(self):
        return f"Message from {self.sender} at {self.timestamp.strftime('%Y-%m-%d %H:%M')}"