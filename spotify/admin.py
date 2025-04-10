from django.contrib import admin
from .models import SpotifyAccount

@admin.register(SpotifyAccount)
class SpotifyAccountAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'account_id', 'last_synced')
    search_fields = ('user_id__username', 'account_id')
    list_filter = ('last_synced',)
