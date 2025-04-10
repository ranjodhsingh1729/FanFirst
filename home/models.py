from django.db import models

# Create your models here.
class SpotifyAccount(models.Model):
    accountId = models.BigIntegerField();
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    last_synced = models.BigIntegerField()
    scope = models.CharField(max_length=255)

