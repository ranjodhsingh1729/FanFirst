from django.db import models
from django.utils import timezone

class Event(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    total_tickets = models.PositiveIntegerField()
    available_tickets = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return f"{self.name} by {self.artist} at {self.venue}"
    
    @property
    def tickets_remaining_percentage(self):
        """Calculate the percentage of tickets remaining"""
        if self.total_tickets == 0:
            return 0
        return (self.available_tickets / self.total_tickets) * 100
    
    @property
    def is_upcoming(self):
        """Check if the event is in the future"""
        return self.date > timezone.now()
