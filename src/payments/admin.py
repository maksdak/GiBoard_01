# src/payments/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Payment

# =================================================================
#  PAYMENT ADMIN
# =================================================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Payment model.
    Financial records should generally be read-only for data integrity.
    """
    list_display = (
        'id',
        'user',
        'amount',
        'currency',
        'status',
        'gateway_name',
        'created_at',
    )
    list_filter = ('status', 'currency', 'gateway_name', 'created_at')
    search_fields = ('user__username', 'user__email', 'id', 'gateway_transaction_id')
    readonly_fields = (
        'id',
        'user',
        'amount',
        'currency',
        'gateway_transaction_id',
        'gateway_name',
        'created_at',
        'updated_at',
    )
    
    # Allow admins to change the status (e.g., for manual refunds)
    # 'status' is not in readonly_fields

    def has_add_permission(self, request):
        # Payments should be created via the payment gateway, not manually.
        return False