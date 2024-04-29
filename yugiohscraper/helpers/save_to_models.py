from sets.models import Set, SetScrapeRecord
from cards.models import Card, CardImage, PriceHistory
from datetime import datetime, date
from django.utils import timezone
from django.db import transaction
import os

def old_sets_save_to_model(sets_data):
    for x in sets_data:
        # Try to retrieve an existing set by link
        set_obj, created = Set.objects.get_or_create(
            link=x.get('link'),
            defaults={
                'title': x.get('title'),
                'type': x.get('type'),
                'updated': datetime.now()
            }
        )

        if not created:
            # If the set exists, update it if necessary
            if (set_obj.title != x.get('title') or 
                set_obj.type != x.get('type')):

                set_obj.title = x.get('title')
                set_obj.type = x.get('type')
                set_obj.updated = datetime.now()
                set_obj.save()
                print(f"Set '{set_obj.title}' updated.")
            else:
                print(f"Set '{set_obj.title}' already up-to-date, no changes made.")
        else:
            print(f"Set '{set_obj.title}' created.")
    
    # Create a SetScrapeRecord object
    SetScrapeRecord.objects.create(timestamp=datetime.now())
    print('Sets data saved to model.')

def sets_save_to_model(sets_data):
    current_time = timezone.now()
    created_updated = False
    for x in sets_data:
        set_obj, created = Set.objects.update_or_create(
            link=x.get('link'),
            defaults={
                'title': x.get('title'),
                'type': x.get('type'),
                'updated': current_time
            }
        )

        if created:
            print(f"Set '{set_obj.title}' created.")
            created_updated = True
        elif (set_obj.title != x.get('title') or set_obj.type != x.get('type')):
            set_obj.title = x.get('title')
            set_obj.type = x.get('type')
            set_obj.updated = current_time
            set_obj.save()
            print(f"Set '{set_obj.title}' updated.")
            created_updated = True
    if created_updated:
        print('Sets updated / created')
    else:
        print('Up to date! No sets created or updated')

def cards_save_to_model(cards_data):
    cards_to_update = []

    # List to store CardImage objects to be created
    card_images_to_create = []

    for x in cards_data:
        set_title = x.get('card-set')
        set_obj = Set.objects.get(title=set_title)

        try:
            card_obj = Card.objects.get(card_link=x.get('card-link'))

            # Check if any of the fields have changed
            if (card_obj.tcg_num_listings != x.get('tcg-num-listings') or
                card_obj.card_rarity != x.get('card-rarity')):

                cards_to_update.append(Card(
                    id=card_obj.id,
                    tcg_num_listings=x.get('tcg-num-listings'),
                    card_rarity=x.get('card-rarity')
                ))
        except Card.DoesNotExist:
            # Create a new Card object
            card_obj = Card.objects.create(
                set=set_obj,
                card_name=x.get('card-name'),
                card_link=x.get('card-link'),
                card_code=x.get('card-code'),
                card_rarity=x.get('card-rarity'),
                tcg_num_listings=x.get('tcg-num-listings')
            )
            print(f"Card '{card_obj}' created.")

        # Create or update CardImage
        file_name = x.get('card-img-path')
        file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
        if os.path.exists(file_path):
            card_image_obj, created = CardImage.objects.get_or_create(card=card_obj)
            card_image_obj.image_path = file_path
            card_image_obj.save()
            print(f"Image for Card '{card_obj}' saved.")
        else:
            print(f"Image file '{file_name}' does not exist.")

    # Bulk update existing cards
    if cards_to_update:
        Card.objects.bulk_update(cards_to_update, ['tcg_num_listings', 'card_rarity'])
        print(f'cards data for {set_title} updated')
    
    print('All cards data saved to model.')

def save_card_prices_to_model(cards_data):
    for card_data in cards_data:
        card_link = card_data.get('card-link')
        tcg_market_price = card_data.get('tcg-market-price')
        tcg_min_listing = card_data.get('tcg-min-listing')
        
        try:
            card = Card.objects.get(card_link=card_link)
            price_history = PriceHistory.objects.create(
                card=card,
                tcg_market_price=tcg_market_price,
                tcg_min_listing=tcg_min_listing,
                date=date.today()
            )
            print(f"Price history for '{card}' saved.")
        except Card.DoesNotExist:
            print(f"Card with link '{card_link}' does not exist.")

    print('All card prices data saved to PriceHistory.')

def save_cards_save_to_model(cards_data):
    cards_to_update = []

    # List to store CardImage objects to be created
    card_images_to_create = []

    for x in cards_data:
        set_title = x.get('card-set')
        set_obj = Set.objects.get(title=set_title)

        try:
            card_obj = Card.objects.get(card_link=x.get('card-link'))

            # Check if any of the fields have changed
            if (card_obj.tcg_market_price != x.get('tcg-market-price') or
                card_obj.tcg_min_listing != x.get('tcg-min-listing') or
                card_obj.tcg_num_listings != x.get('tcg-num-listings') or
                card_obj.card_rarity != x.get('card-rarity')):

                cards_to_update.append(Card(
                    id=card_obj.id,
                    tcg_market_price=x.get('tcg-market-price'),
                    tcg_min_listing=x.get('tcg-min-listing'),
                    tcg_num_listings=x.get('tcg-num-listings'),
                    card_rarity=x.get('card-rarity')
                ))
        except Card.DoesNotExist:
            # Create a new Card object
            card_obj = Card.objects.create(
                set=set_obj,
                card_name=x.get('card-name'),
                card_link=x.get('card-link'),
                card_code=x.get('card-code'),
                card_rarity=x.get('card-rarity'),
                tcg_market_price=x.get('tcg-market-price'),
                tcg_min_listing=x.get('tcg-min-listing'),
                tcg_num_listings=x.get('tcg-num-listings')
            )
            print(f"Card '{card_obj}' created.")

        # Create or update CardImage
        file_name = x.get('card-img-path')
        file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
        if os.path.exists(file_path):
            card_image_obj, created = CardImage.objects.get_or_create(card=card_obj)
            card_image_obj.image_path = file_path
            card_image_obj.save()
            print(f"Image for Card '{card_obj}' saved.")
        else:
            print(f"Image file '{file_name}' does not exist.")

    # Bulk update existing cards
    if cards_to_update:
        Card.objects.bulk_update(cards_to_update, ['tcg_market_price', 'tcg_min_listing', 'tcg_num_listings'])
        print(f'cards data for {set_title} updated')
    
    print('All cards data saved to model.')


def maybe_cards_save_to_model(cards_data):
    cards_to_update = []


    for x in cards_data:
        set_title = x.get('card-set')
        set_obj = Set.objects.get(title=set_title)

        try:
            card_obj = Card.objects.get(card_link=x.get('card-link'))

            # Check if any of the fields have changed
            if (card_obj.tcg_market_price != x.get('tcg-market-price') or
                card_obj.tcg_min_listing != x.get('tcg-min-listing') or
                card_obj.tcg_num_listings != x.get('tcg-num-listings')):

                cards_to_update.append(Card(
                    id=card_obj.id,
                    tcg_market_price=x.get('tcg-market-price'),
                    tcg_min_listing=x.get('tcg-min-listing'),
                    tcg_num_listings=x.get('tcg-num-listings')
                ))
                card_image_obj = CardImage.objects.filter(card=card_obj).last()
                if card_image_obj.image_path and 'default.jpg' in card_image_obj.image_path:
                    file_name = x.get('card-img-path')
                    file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
                    if os.path.exists(file_path):
                        card_image_obj = CardImage(card=card_obj, image_path=file_path)
                        card_image_obj.save()
                        print(f"Image for Card '{card_obj}' saved.")
                    else:
                        print(f"Image file '{file_name}' does not exist.")
        except Card.DoesNotExist:
            card_obj = Card.objects.create(
                set=set_obj,
                card_name=x.get('card-name'),
                card_link=x.get('card-link'),
                card_code=x.get('card-code'),
                card_rarity=x.get('card-rarity'),
                tcg_market_price=x.get('tcg-market-price'),
                tcg_min_listing=x.get('tcg-min-listing'),
                tcg_num_listings=x.get('tcg-num-listings')
            )
            print(f"Card '{card_obj}' created.")
            try:
                card_obj = Card.objects.get(card_link=x.get('card-link'))
                card_image_obj = CardImage.objects.filter(card=card_obj).last()
                if card_image_obj:
                    print(f"Image for Card '{card_obj}' already exists.")
                    file_name = x.get('card-img-path')
                    file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
                    card_image_obj.image_path = file_path
                    card_image_obj.save()
                    print(f"Image for Card '{card_obj}' saved.")
                else:
                    # If the card image doesn't exist, create a new one
                    file_name = x.get('card-img-path')
                    file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
                    if os.path.exists(file_path):
                        card_image_obj = CardImage(card=card_obj, image_path=file_path)
                        card_image_obj.save()
                        print(f"Image for Card '{card_obj}' saved.")
                    else:
                        print(f"Image file '{file_name}' does not exist.")
            except CardImage.DoesNotExist:
                # If the card image doesn't exist, create a new one
                file_name = x.get('card-img-path')
                file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
                if os.path.exists(file_path):
                    card_image_obj = CardImage(card=card_obj, image_path=file_path)
                    card_image_obj.save()
                    print(f"Image for Card '{card_obj}' saved.")
                else:
                    print(f"Image file '{file_name}' does not exist.")
    # Bulk update existing cards
    if cards_to_update:
        Card.objects.bulk_update(cards_to_update, ['tcg_market_price', 'tcg_min_listing', 'tcg_num_listings'])
        print(f'cards data for {set_title} updated')
        
    print('All cards data saved to model.')


def old_cards_save_to_model(cards_data):
    for x in cards_data:
        set_title = x.get('card-set')
        set_obj = Set.objects.get(title=set_title)

        # Try to retrieve an existing card by card_link
        try:
            card_obj = Card.objects.get(card_link=x.get('card-link'))
        except Card.DoesNotExist:
            # If the card doesn't exist, create a new one
            card_obj = Card.objects.create(
                set=set_obj,
                card_name=x.get('card-name'),
                card_link=x.get('card-link'),
                card_code=x.get('card-code'),
                card_rarity=x.get('card-rarity'),
                tcg_market_price=x.get('tcg-market-price'),
                tcg_min_listing=x.get('tcg-min-listing'),
                tcg_num_listings=x.get('tcg-num-listings')
            )
            print(f"Card '{card_obj}' created.")
        else:
            # Update the existing card if necessary
            if (card_obj.card_name != x.get('card-name') or
                card_obj.card_code != x.get('card-code') or
                card_obj.card_rarity != x.get('card-rarity') or
                card_obj.tcg_market_price != x.get('tcg-market-price') or
                card_obj.tcg_min_listing != x.get('tcg-min-listing') or
                card_obj.tcg_num_listings != x.get('tcg-num-listings')):

                card_obj.card_name = x.get('card-name')
                card_obj.card_code = x.get('card-code')
                card_obj.card_rarity = x.get('card-rarity')
                card_obj.tcg_market_price = x.get('tcg-market-price')
                card_obj.tcg_min_listing = x.get('tcg-min-listing')
                card_obj.tcg_num_listings = x.get('tcg-num-listings')
                card_obj.save()
                print(f"Card '{card_obj}' updated.")
            else:
                print(f"Card '{card_obj}' already up-to-date, no changes made.")

        # Save the image to CardImage model
        try:
            card_image_obj = CardImage.objects.get(card=card_obj)
        except CardImage.DoesNotExist:
            # If the card image doesn't exist, create a new one
            file_name = x.get('card-img-path')
            file_path = os.path.join('staticfiles-cdn/card-imgs/sets', file_name)
            if os.path.exists(file_path):
                card_image_obj = CardImage(card=card_obj, image_path=file_path)
                card_image_obj.save()
                print(f"Image for Card '{card_obj}' saved.")
            else:
                print(f"Image file '{file_name}' does not exist.")
        else:
            print(f"Image for Card '{card_obj}' already exists.")

    print('Cards data saved to model.')

def old_card_details_save_to_model(card_details_data):

    for x in card_details_data:

        try:
            card = Card.objects.get(id = x.get('card_id'))
        except card.DoesNotExist:
            print('No card saved with ID provided')
            continue

        if ( card.lore != x.get('lore') or
            card.card_type != x.get('type') or
            card.simple_type != x.get('simple_type') or
            card.attribute != x.get('attribute') or 
            card.archtype != x.get('archtype') or
            card.level != x.get('level') or
            card.card_atk != x.get('atk') or
            card.card_def != x.get('def') ):
            
            card.lore = x.get('lore')
            card.card_type = x.get('type')
            card.simple_type = x.get('simple_type')
            card.attribute = x.get('attribute') 
            card.archtype = x.get('archtype')
            card.level = x.get('level')
            card.card_atk = x.get('atk')
            card.card_def = x.get('def')
            card.save()
            print(f'Card: ({card.card_name}) updated with futher details.')

        else:
            print(f'Card: ({card.card_name}) details already up to date.')
    print('All cards details saved or updated!')

def card_details_save_to_model(card_details_data):
    cards_to_update = []

    for x in card_details_data:
        try:
            card = Card.objects.get(id=x.get('card_id'))
        except Card.DoesNotExist:
            print('No card saved with ID provided')
            continue

        if (card.lore != x.get('lore') or
                card.card_type != x.get('type') or
                card.simple_type != x.get('simple_type') or
                card.attribute != x.get('attribute') or
                card.archtype != x.get('archtype') or
                card.level != x.get('level') or
                card.card_atk != x.get('atk') or
                card.card_def != x.get('def')):

            card.lore = x.get('lore')
            card.card_type = x.get('type')
            card.simple_type = x.get('simple_type')
            card.attribute = x.get('attribute')
            card.archtype = x.get('archtype')
            card.level = x.get('level')
            card.card_atk = x.get('atk')
            card.card_def = x.get('def')
            cards_to_update.append(card)

    if cards_to_update:
        Card.objects.bulk_update(cards_to_update, fields=[
            'lore', 'card_type', 'simple_type', 'attribute',
            'archtype', 'level', 'card_atk', 'card_def'
        ])
        print('All cards details saved or updated!')
    else:
        print('No card details to update.')