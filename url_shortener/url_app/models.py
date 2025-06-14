from django.db import models
from datetime import date
from datetime import datetime
from django.contrib.auth.models import User

#* ===== MODELS ===== *#
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class ShortenedUrl(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    custom_code = models.CharField(max_length=20, unique=True, null=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    max_uses = models.IntegerField(null=True, blank=True)
    current_uses = models.IntegerField(default=0, null=True)
    url_password  = models.CharField(max_length=128, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    qr_code = models.ImageField(blank=True, null=True)