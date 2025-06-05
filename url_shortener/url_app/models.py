from django.db import models
from datetime import date
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
    custom_code = models.CharField(max_length=20, unique=True, null=True, blank=False)
    expiry_date = models.DateTimeField()
    max_uses = models.IntegerField(null=True, blank=True)
    current_uses = models.IntegerField(default=0)
    url_password  = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)