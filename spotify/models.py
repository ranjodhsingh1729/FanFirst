from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class SpotifyAccount(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    account_id = models.CharField(max_length=255)
    expires_in = models.BigIntegerField()
    expires_at = models.BigIntegerField()
    last_synced = models.BigIntegerField()
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_type = models.CharField(max_length=255)
    scope = models.CharField(max_length=255)
