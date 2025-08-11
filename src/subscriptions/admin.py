# src/subscriptions/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Plan, Subscription

# =================================================================
#  PLAN ADMIN
# =================================================================

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Plan model.
    """
    list_display = ('name', 'price', 'duration_days', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')

# =================================================================
#  SUBSCRIPTION ADMIN
# =================================================================

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Subscription model.
    """
    list_display = ('user', 'plan', 'start_date', 'end_date', 'status', 'is_currently_active')
    list_filter = ('status', 'plan', 'start_date', 'end_date')
    search_fields = ('user__username', 'user__email', 'plan__name')
    autocomplete_fields = ('user', 'plan') # For easier selection
    readonly_fields = ('start_date', 'end_date')

    def is_currently_active(self, obj):
        """
        A boolean method to show in the list_display if the subscription
        is factually active right now.
        """
        return obj.is_active
    is_currently_active.boolean = True # Displays a nice icon (tick/cross)
    is_currently_active.short_description = _('Currently Active?')