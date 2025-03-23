# # yourapp/management/commands/copy_media_to_static.py
# import os
# import shutil
# from django.core.management.base import BaseCommand
# from django.conf import settings

# class Command(BaseCommand):
#     help = 'Copy media files to whitenoise static root for serving'

#     def handle(self, *args, **options):
#         source_dir = settings.MEDIA_ROOT
#         target_dir = settings.WHITENOISE_ROOT
        
#         # Create target directory if it doesn't exist
#         os.makedirs(target_dir, exist_ok=True)
        
#         # Count for reporting
#         copied = 0
        
#         # Walk through all files in media directory
#         for root, dirs, files in os.walk(source_dir):
#             for file in files:
#                 source_path = os.path.join(root, file)
#                 # Get relative path from MEDIA_ROOT
#                 rel_path = os.path.relpath(source_path, source_dir)
#                 target_path = os.path.join(target_dir, rel_path)
                
#                 # Ensure target directory exists
#                 os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
#                 # Copy the file
#                 shutil.copy2(source_path, target_path)
#                 copied += 1
#                 self.stdout.write(f"Copied: {rel_path}")
        
#         self.stdout.write(self.style.SUCCESS(f'Successfully copied {copied} files'))