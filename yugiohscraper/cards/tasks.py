
from celery import shared_task
import helpers
import time

@shared_task
def old_scrape_parse_save_cards(url):
    time.sleep(2)  # Optional delay to avoid overloading the server
    sets_cards_data = helpers.main_set_cards(url)
    helpers.cards_save_to_model(sets_cards_data)
    
@shared_task
def scrape_parse_save_cards(url):
    time.sleep(2)  # Optional delay to avoid overloading the server
    sets_cards_data = helpers.main_set_cards(url)
    helpers.cards_save_to_model(sets_cards_data)
    helpers.save_card_prices_to_model(sets_cards_data)
    return


@shared_task
def scrape_parse_save_sets():
    url = 'https://shop.tcgplayer.com/yugioh?newSearch=true&_gl=1*sgexa9*_gcl_au*MzcyOTUwOTU3LjE3MTA5MjM5MzA.*_ga*MTk3NTI4NjUyMy4xNzEwOTIzOTMw*_ga_VS9BE2Z3GY*MTcxMzM0MzE2MC40Mi4wLjE3MTMzNDMxNjAuNjAuMC4w'
    html_soup = helpers.scrape_yugioh_sets(url)
    sets_data = helpers.parse_yugioh_sets(html_soup)
    helpers.sets_save_to_model(sets_data)
    return

@shared_task
def scrape_parse_save_card_details(url):
    set_cards_details_data = helpers.main_set_cards_details(url)
    helpers.card_details_save_to_model(set_cards_details_data)
    return

