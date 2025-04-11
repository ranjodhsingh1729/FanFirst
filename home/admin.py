from django.contrib import admin
from . import models
# Register your models here.
@admin.register(models.Event)
class SpotifyAccountAdmin(admin.ModelAdmin):
    pass
