from celery import shared_task
from celery.result import allow_join_result

import helpers

from .models import Set
from cards.models import Card
from cards.tasks import scrape_parse_save_cards, scrape_parse_save_card_details

@shared_task
def scrape_yugioh_sets():
    url = 'https://shop.tcgplayer.com/yugioh?newSearch=true&_gl=1*a98xor*_gcl_au*MzcyOTUwOTU3LjE3MTA5MjM5MzA.*_ga*MTk3NTI4NjUyMy4xNzEwOTIzOTMw*_ga_VS9BE2Z3GY*MTcxMTM2NjE0My4zLjAuMTcxMTM2NjE0My42MC4wLjA.'
    html = helpers.scrape_yugioh_sets(url)
    sets_data = helpers.parse_yugioh_sets(html)
    helpers.sets_save_to_model(sets_data)
    return

@shared_task
def testing_main_scrape_cards_and_details():
    set_links = Set.objects.values_list('link', flat=True)
    test_set_links = list(set_links[:3]) + [set_links[4]]

    chunk_size = 2
    url_chunks = [test_set_links[i:i + chunk_size] for i in range(0, len(test_set_links), chunk_size)]

    for url_chunk in url_chunks:
        cards_tasks = []
        for url in url_chunk:
            cards_task = scrape_parse_save_cards.delay(url)
            cards_tasks.append(cards_task)
        with allow_join_result():
            completed = [task_result.get() for task_result in cards_tasks]

        details_tasks = []
        for url in url_chunk:
            details_task = scrape_parse_save_card_details.delay(url)
            details_tasks.append(details_task)
        with allow_join_result():
            completed = [task_result.get() for task_result in details_tasks]

@shared_task
def main_scrape_cards_and_details():
    set_links = Set.objects.values_list('link', flat=True)
    # test_set_links = [list(set_links)[-1]] + list(set_links[:3]) + list(set_links[4:11])
    test_set_links = [list(set_links)[-1]] + [list(set_links)[0]]

    chunk_size = 2
    url_chunks = [test_set_links[i:i + chunk_size] for i in range(0, len(test_set_links), chunk_size)]

    for url_chunk in url_chunks:
        cards_tasks = []
        for url in url_chunk:
            cards_task = scrape_parse_save_cards.delay(url)
            cards_tasks.append(cards_task)
        with allow_join_result():
            completed = [task_result.get() for task_result in cards_tasks]

        details_tasks = []
        for url in url_chunk:
            set_name = Set.objects.values_list('title', flat=True).filter(link=str(url)).first()
            set_last_card = Card.objects.filter(set__link = str(url)).values_list('lore', flat=True).last()
            if set_last_card == None:
                print(f'No Card Details for {set_name}')
                details_task = scrape_parse_save_card_details.delay(url)
                details_tasks.append(details_task)
                # with allow_join_result():
                #     completed = [task_result.get() for task_result in details_tasks]
            else:
                print(f'Already have Card Details for {set_name}')
        if details_tasks:
            with allow_join_result():
                completed = [task_result.get() for task_result in details_tasks]

@shared_task
def simulated_qcr_core_sets_booster_stats():
    phni = Card.objects.filter(set__link='https://www.tcgplayer.com/search/yugioh/phantom-nightmare')
    agov = Card.objects.filter(set__link='https://www.tcgplayer.com/search/yugioh/age-of-overlord')
    dune = Card.objects.filter(set__link='https://www.tcgplayer.com/search/yugioh/duelist-nexus')
    lede = Card.objects.filter(set__link='https://www.tcgplayer.com/search/yugioh/legacy-of-destruction')
    qcr_core_sets = [phni, agov, dune, lede]

    num_iterations = 10000
    sets_booster_stats_data = []
    for qcr_core_set in qcr_core_sets:
        set_first_card = qcr_core_set[0]
        set_booster_price = set_first_card.set.average_price
        list_qcr_core_set = [[card.card_rarity, card.get_market_price()] for card in qcr_core_set]
        simulated_values = helpers.simulate_multiple_boxes(list_qcr_core_set, num_iterations)
        set_booster_stats_data = helpers.stats_for_simulated_set(simulated_values, set_booster_price)
        print(set_booster_stats_data)
        sets_booster_stats_data.append({
            'set_name': str(set_first_card.set.title),
            'set_booster_stats_data': set_booster_stats_data
        })
    return sets_booster_stats_data