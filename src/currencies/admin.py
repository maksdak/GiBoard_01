from django.contrib import admin
from .models import CurrencyRate

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('source_currency', 'target_currency', 'rate', 'last_updated')
    list_filter = ('source_currency', 'target_currency')