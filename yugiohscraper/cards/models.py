from django.db import models
from sets.models import Set


class Card(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=200)
    card_link = models.URLField()
    card_rarity = models.CharField(max_length=50)
    card_code = models.CharField(max_length=20)
    # tcg_market_price = models.DecimalField(max_digits=10, decimal_places=2)
    # tcg_min_listing = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tcg_num_listings = models.IntegerField(null=True)
    
    # Card details
    lore = models.CharField(max_length=1000, default=None, blank=True, null=True)
    card_type = models.CharField(max_length=100, default=None, blank=True, null=True)
    simple_type = models.CharField(max_length=50, default=None, blank=True, null=True)
    attribute = models.CharField(max_length=50, default=None, blank=True, null=True)
    archtype = models.CharField(max_length=50, default=None, blank=True, null=True)
    level = models.CharField(max_length=10, default=None, blank=True, null=True)
    card_atk = models.CharField(max_length=10, default=None, blank=True, null=True)
    card_def = models.CharField(max_length=10, default=None, blank=True, null=True)

    # 

    def __str__(self):
        return f'{self.card_name} - {self.card_rarity}'
    
    def get_image(self):
        card_image = CardImage.objects.filter(card__id=self.id).last()
        image = 'card-imgs/sets/default.jpg'
        if card_image is not None:
            image_raw = card_image.image_path
            image_path_list = image_raw.split('/')
            image = '/'.join(image_path_list[1:])
        return image
    
    def get_market_price(self):
        # Get the latest price history entry for this card
        latest_price = self.pricehistory_set.order_by('-date').first()
        if latest_price:
            return latest_price.tcg_market_price
        else:
            return None

    def get_min_listing(self):
        # Get the latest price history entry for this card
        latest_price = self.pricehistory_set.order_by('-date').first()
        if latest_price:
            return latest_price.tcg_min_listing
        else:
            return None


class CardImage(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=400)


class PriceHistory(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    tcg_market_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tcg_min_listing = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank = True)
    
    def __str__(self):
        return f'{self.card.card_name} - {self.date}'
    
class CardProbability(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    pull_probability_per_booster = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.pull_probability_per_booster} - {self.card.card_name} - {self.card.card_rarity} - {self.set.title}"

    @classmethod
    def update_probabilities(cls, set_link, probabilities):
        cards = Card.objects.filter(set__link=set_link)

        for rarity, probability in probabilities.items():
            print(rarity, probability)
            set_cards_by_rarity = cards.filter(card_rarity=rarity)
            for card in set_cards_by_rarity:
                try:
                    card_prob_object = CardProbability.objects.get(
                        card = card,
                        set = Set.objects.get(link = set_link),
                    )
                    print(f'Already have probability for {card.card_name}')
                    # print('created card prob')
                except CardProbability.DoesNotExist:
                    CardProbability.objects.create(
                        card=card,
                        set = Set.objects.get(link = set_link),
                        pull_probability_per_booster = probability
                    )
                    print('created card prob')