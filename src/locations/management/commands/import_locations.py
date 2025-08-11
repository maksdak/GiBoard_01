# src/locations/management/commands/import_locations.py

import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from locations.models import Country, City

class Command(BaseCommand):
    help = 'Imports countries and cities from a JSON file'

    def handle(self, *args, **options):
        file_path = 'data/locations.json'
        self.stdout.write(self.style.SUCCESS(f'Starting location import from {file_path}...'))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}.'))
            return

        created_countries = 0
        created_cities = 0

        for entry in data:
            # Create Country
            country, created = Country.objects.get_or_create(
                code=entry['country_code'],
                defaults={'name': entry['country_name']}
            )
            if created:
                created_countries += 1
                self.stdout.write(f'  Created country: {country.name}')

            # Create Cities
            for city_data in entry.get('cities', []):
                location_data = city_data.get('location')
                point = None
                if location_data:
                    point = Point(location_data['longitude'], location_data['latitude'])

                city, created = City.objects.get_or_create(
                    name=city_data['name'],
                    country=country,
                    defaults={'location': point}
                )
                if created:
                    created_cities += 1
                    self.stdout.write(f'    - Created city: {city.name}')

        self.stdout.write(self.style.SUCCESS(
            f'Import complete. Countries created: {created_countries}, Cities created: {created_cities}'
        ))