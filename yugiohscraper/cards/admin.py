from django.contrib import admin
from .models import Card, CardImage
# Register your models here.

class CardAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'card_code',
        'card_name',
        #'tcg_market_price',
        'card_rarity',
    ]

admin.site.register(Card, CardAdmin)
admin.site.register(CardImage)