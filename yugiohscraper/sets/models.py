from django.db import models
from django.urls import reverse
# Create your models here.
class Set(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    code = models.CharField(max_length=10, blank=True, null=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.link[0:50]
    
    def get_absolute_url(self):
        return reverse("set-detail", kwargs={"id": self.id})
    
class SetScrapeRecord(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.timestamp}'
    
