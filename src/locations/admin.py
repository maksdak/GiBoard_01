# src/locations/admin.py

from django.contrib.gis import admin
from .models import Country, City

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(City)
class CityAdmin(admin.ModelAdmin): # <-- THE ONLY CHANGE IS HERE
    list_display = ('name', 'country')
    list_filter = ('country',)
    search_fields = ('name',)
    # These settings help to center the map by default
    default_lon = -5.353585
    default_lat = 36.140751
    default_zoom = 12