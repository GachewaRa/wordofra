from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.throttling import AnonRateThrottle
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=150, unique=True)
    is_newsletter_subscribed = models.BooleanField(default=False) 
    # Fields for login attempt tracking
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'username']
    
    def increment_failed_login(self):
        """Increment the failed login attempts counter and update timestamp."""
        self.failed_login_attempts += 1
        self.last_failed_login = timezone.now()
        self.save(update_fields=['failed_login_attempts', 'last_failed_login'])
        return self.failed_login_attempts
    
    def reset_failed_login(self):
        """Reset the failed login attempts counter."""
        self.failed_login_attempts = 0
        self.save(update_fields=['failed_login_attempts'])
        
    def is_account_locked(self):
        """Check if the account is locked due to too many failed attempts."""
        if self.failed_login_attempts >= 5:
            if self.last_failed_login and self.last_failed_login + timedelta(minutes=30) > timezone.now():
                return True
            else:
                # Lockout period expired, reset the counter
                self.reset_failed_login()
        return False

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

@receiver(post_save, sender=CustomUser)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})" if self.name else self.email


class LoginRateThrottle(AnonRateThrottle):
    rate = '5/hour'
    scope = 'login_attempts'