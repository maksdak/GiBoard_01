# src/categories/management/commands/import_categories.py

import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from categories.models import Category

class Command(BaseCommand):
    help = 'Imports categories from a JSON file into the database'

    def handle(self, *args, **options):
        # Path to the JSON file, relative to the project root
        file_path = 'data/categories.json'
        
        self.stdout.write(self.style.SUCCESS(f'Starting category import from {file_path}...'))

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found: {file_path}. Make sure the file exists.'))
            return
        
        created_count = 0
        
        for entry in data:
            # Create parent category
            parent_name = entry.get('name')
            parent_slug = entry.get('slug', slugify(parent_name))
            
            parent_cat, created = Category.objects.get_or_create(
                name=parent_name,
                slug=parent_slug,
                defaults={'parent': None} # Ensure it's a root node
            )
            
            if created:
                created_count += 1
                self.stdout.write(f'  Created root category: {parent_cat.name}')
            
            # Create children categories
            for child_entry in entry.get('children', []):
                child_name = child_entry.get('name')
                child_slug = child_entry.get('slug', slugify(child_name))
                
                child_cat, created = Category.objects.get_or_create(
                    name=child_name,
                    slug=child_slug,
                    defaults={'parent': parent_cat}
                )

                if created:
                    created_count += 1
                    self.stdout.write(f'    - Created child category: {child_cat.name} under {parent_cat.name}')

        self.stdout.write(self.style.SUCCESS(f'Import complete. Total new categories created: {created_count}'))