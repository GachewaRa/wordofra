"""
Django management command: Extracts base64 images from blog post content,
uploads them to Cloudinary, and replaces the data URIs with Cloudinary URLs.
"""
import re
import base64
import cloudinary.uploader
from django.core.management.base import BaseCommand
from blog.models import Post


BASE64_IMG_PATTERN = re.compile(
    r'(<img[^>]+src=")data:image/([a-zA-Z]+);base64,([^"]+)("[^>]*>)'
)


class Command(BaseCommand):
    help = "Convert base64 images in blog post content to Cloudinary URLs"

    def handle(self, *args, **options):
        posts = Post.objects.all()
        self.stdout.write(f"Checking {posts.count()} posts for base64 images...")

        for post in posts:
            matches = list(BASE64_IMG_PATTERN.finditer(post.content))
            if not matches:
                self.stdout.write(f"  [{post.slug}] No base64 images found.")
                continue

            self.stdout.write(f"  [{post.slug}] Found {len(matches)} base64 image(s). Uploading...")
            updated_content = post.content

            for i, match in enumerate(matches):
                prefix = match.group(1)      # <img ... src="
                img_format = match.group(2)   # jpeg, png, etc.
                b64_data = match.group(3)     # the base64 string
                suffix = match.group(4)       # " ... >

                try:
                    image_bytes = base64.b64decode(b64_data)
                    result = cloudinary.uploader.upload(
                        image_bytes,
                        folder=f"blog/{post.slug}",
                        public_id=f"content_img_{i}",
                        resource_type="image",
                        overwrite=True,
                    )
                    cloudinary_url = result["secure_url"]
                    self.stdout.write(f"    Uploaded image {i} -> {cloudinary_url}")

                    old_full = match.group(0)
                    new_full = f'{prefix}{cloudinary_url}{suffix}'
                    updated_content = updated_content.replace(old_full, new_full, 1)

                except Exception as e:
                    self.stderr.write(f"    ERROR uploading image {i}: {e}")
                    continue

            if updated_content != post.content:
                old_size = len(post.content)
                new_size = len(updated_content)
                post.content = updated_content
                post.save(update_fields=["content"])
                self.stdout.write(
                    self.style.SUCCESS(
                        f"    Saved! Content: {old_size:,} -> {new_size:,} bytes "
                        f"({(1 - new_size/old_size)*100:.1f}% reduction)"
                    )
                )

        self.stdout.write(self.style.SUCCESS("Done!"))
