from django.contrib import admin
from .models import Set, SetScrapeRecord
# Register your models here.

class SetAdmin(admin.ModelAdmin):
    list_display=[
        'id',
        'title',
        'link',
        'type',
        'updated',
    ]
admin.site.register(Set, SetAdmin)
admin.site.register(SetScrapeRecord)