"""
Management command to migrate existing local images to Supabase Storage.
Usage: python manage.py migrate_images_to_supabase
"""
from django.core.management.base import BaseCommand
from donations.models import Donation
from django.core.files import File
import os


class Command(BaseCommand):
    help = 'Migrate existing local images to Supabase Storage'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Starting image migration to Supabase Storage...'))
        
        # Get all donations with images
        donations = Donation.objects.exclude(image='').exclude(image__isnull=True)
        total = donations.count()
        migrated = 0
        skipped = 0
        
        self.stdout.write(f'Found {total} donations with images')
        
        for donation in donations:
            # Check if file exists locally
            local_path = donation.image.path if hasattr(donation.image, 'path') else None
            
            if local_path and os.path.exists(local_path):
                try:
                    # Re-save the image (this will trigger upload to Supabase)
                    with open(local_path, 'rb') as f:
                        file_name = os.path.basename(local_path)
                        donation.image.save(file_name, File(f), save=True)
                    
                    migrated += 1
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Migrated: {donation.medicine_name} - {file_name}')
                    )
                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(f'✗ Failed to migrate {donation.medicine_name}: {str(e)}')
                    )
            else:
                skipped += 1
                self.stdout.write(
                    self.style.WARNING(f'⊘ Skipped {donation.medicine_name}: Local file not found')
                )
        
        self.stdout.write(self.style.SUCCESS(f'\n✅ Migration complete!'))
        self.stdout.write(f'Migrated: {migrated}')
        self.stdout.write(f'Skipped: {skipped}')
        self.stdout.write(f'Total: {total}')
