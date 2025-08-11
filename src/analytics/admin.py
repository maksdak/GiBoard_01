# src/analytics/admin.py

from django.contrib import admin
from .models import PageView

# =================================================================
#  PAGE VIEW ADMIN
# =================================================================

@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    """
    Admin configuration for the PageView model.
    This model should be read-only as data is collected automatically.
    """
    list_display = ('url_path', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('url_path',)
    readonly_fields = ('url_path', 'timestamp')

    def has_add_permission(self, request):
        # Disable the "Add" button in the admin
        return False

    def has_change_permission(self, request, obj=None):
        # Disable the "Change" functionality
        return False

    # Optional: We can still allow deletion if needed
    # def has_delete_permission(self, request, obj=None):
    #     return True