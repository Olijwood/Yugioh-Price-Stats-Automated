from sets.models import Set
from cards.models import Card

phni = Card.objects.filter(set__link = 'https://www.tcgplayer.com/search/yugioh/phantom-nightmare')

def core_qcr_calculate_odds_per_booster_box(set_cards):

    num_common = len(set_cards.filter(card_rarity = 'Common'))
    print('Set contains:' + str(num_common) + 'Commons')
    num_super = len(set_cards.filter(card_rarity = 'Super Rare'))
    print('Set contains:' + str(num_super) + 'Supers')
    num_ultra = len(set_cards.filter(card_rarity = 'Ultra Rare'))
    print('Set contains:' + str(num_ultra) + 'Ultras')
    num_secret = len(set_cards.filter(card_rarity = 'Secret Rare'))
    print('Set contains:' + str(num_secret) + 'Secrets')
    num_qcr = len(set_cards.filter(card_rarity = 'Quarter Century'))
    print('Set contains:' + str(num_qcr) + 'QCRs')

    total_cards_per_pack = 9
    total_packs_per_booster_box = 24
    total_cards_per_booster_box = total_cards_per_pack * total_packs_per_booster_box
    print(str(total_cards_per_booster_box) + 'Total cards per box')

    num_secret_rare_per_booster_box = 2
    num_ultra_rare_per_booster_box = 4
    num_super_rare_per_booster_box = 18
    num_common_per_booster_box = total_cards_per_booster_box - (
                                            num_secret_rare_per_booster_box +
                                            num_ultra_rare_per_booster_box +
                                            num_super_rare_per_booster_box)
   
    probability_qcr = 1 / (total_cards_per_booster_box * 4)
    probability_secret_rare = num_secret_rare_per_booster_box / total_cards_per_booster_box
    probability_ultra_rare = num_ultra_rare_per_booster_box / total_cards_per_booster_box
    probability_super_rare = num_super_rare_per_booster_box / total_cards_per_booster_box
    probability_common = num_common_per_booster_box / total_cards_per_booster_box

    # Subtract the probability of pulling a QCR from the probabilities of pulling an Ultra Rare or a Secret Rare
    probability_ultra_rare -= probability_qcr/2
    probability_secret_rare -= probability_qcr/2

    print("Odds per booster box for pulling each rarity:")
    print(f"Quarter Century Secret Rare: {probability_qcr:.2%}")
    print(f"Secret Rare: {probability_secret_rare:.2%}")
    print(f"Ultra Rare: {probability_ultra_rare:.2%}")
    print(f"Super Rare: {probability_super_rare:.2%}")
    print(f"Common: {probability_common:.2%}")
    print('Rarity probability_total: ' + str((probability_common + probability_super_rare + 
                                            probability_ultra_rare + probability_secret_rare +
                                            probability_qcr))) 

    probability_specific_qcr = probability_qcr / num_qcr
    probability_specific_secret_rare = probability_secret_rare / num_secret
    probability_specific_ultra_rare = probability_ultra_rare / num_ultra
    probability_specific_super_rare = probability_super_rare / num_super
    probability_specific_common = probability_common / num_common

    print("Odds per booster box for pulling a specific card in that rarity:")
    print(f"Quarter Century Secret Rare: {probability_specific_qcr:.8%}")
    print(f"Secret Rare: {probability_specific_secret_rare:.8%}")
    print(f"Ultra Rare: {probability_specific_ultra_rare:.8%}")
    print(f"Super Rare: {probability_specific_super_rare:.8%}")
    print(f"Common: {probability_specific_common:.8%}")

    specific_card_probabilities = {
        'Common': probability_specific_common,
        'Super Rare': probability_specific_super_rare,
        'Ultra Rare': probability_specific_ultra_rare,
        'Secret Rare': probability_specific_secret_rare,
        'Quarter Century': probability_specific_qcr,
    }

    return specific_card_probabilities

def old_core_qcr_calculate_odds_per_booster_box(set_cards):

    num_common = len(set_cards.filter(card_rarity = 'Common'))
    print('Set contains:' + str(num_common) + 'Commons')
    num_super = len(set_cards.filter(card_rarity = 'Super Rare'))
    print('Set contains:' + str(num_super) + 'Supers')
    num_ultra = len(set_cards.filter(card_rarity = 'Ultra Rare'))
    print('Set contains:' + str(num_ultra) + 'Ultras')
    num_secret = len(set_cards.filter(card_rarity = 'Secret Rare'))
    print('Set contains:' + str(num_secret) + 'Secrets')
    num_qcr = len(set_cards.filter(card_rarity = 'Quarter Century'))
    print('Set contains:' + str(num_qcr) + 'QCRs')

    total_cards_per_pack = 9
    total_packs_per_booster_box = 24
    total_cards_per_booster_box = total_cards_per_pack * total_packs_per_booster_box
    print(str(total_cards_per_booster_box) + 'Total cards per box')

    num_secret_rare_per_booster_box = 2
    num_ultra_rare_per_booster_box = 4
    num_super_rare_per_booster_box = 18
    num_common_per_booster_box = total_cards_per_booster_box - (
                                            num_secret_rare_per_booster_box +
                                            num_ultra_rare_per_booster_box +
                                            num_super_rare_per_booster_box)
   
    probability_qcr = 1 / (total_cards_per_booster_box * 4)
    probability_secret_rare = num_secret_rare_per_booster_box / total_cards_per_booster_box
    probability_ultra_rare = num_ultra_rare_per_booster_box / total_cards_per_booster_box
    probability_super_rare = num_super_rare_per_booster_box / total_cards_per_booster_box
    probability_common = num_common_per_booster_box / total_cards_per_booster_box

    # Subtract the probability of pulling a QCR from the probabilities of pulling an Ultra Rare or a Secret Rare
    probability_ultra_rare -= probability_qcr/2
    probability_secret_rare -= probability_qcr/2

    print("Odds per booster box for pulling each rarity:")
    print(f"Quarter Century Secret Rare: {probability_qcr:.2%}")
    print(f"Secret Rare: {probability_secret_rare:.2%}")
    print(f"Ultra Rare: {probability_ultra_rare:.2%}")
    print(f"Super Rare: {probability_super_rare:.2%}")
    print(f"Common: {probability_common:.2%}")
    print('Rarity probability_total: ' + str((probability_common + probability_super_rare + 
                                            probability_ultra_rare + probability_secret_rare +
                                            probability_qcr))) 

    probability_specific_qcr = probability_qcr / num_qcr
    probability_specific_secret_rare = probability_secret_rare / num_secret
    probability_specific_ultra_rare = probability_ultra_rare / num_ultra
    probability_specific_super_rare = probability_super_rare / num_super
    probability_specific_common = probability_common / num_common

    print("Odds per booster box for pulling a specific card in that rarity:")
    print(f"Quarter Century Secret Rare: {probability_specific_qcr:.8%}")
    print(f"Secret Rare: {probability_specific_secret_rare:.8%}")
    print(f"Ultra Rare: {probability_specific_ultra_rare:.8%}")
    print(f"Super Rare: {probability_specific_super_rare:.8%}")
    print(f"Common: {probability_specific_common:.8%}")
    
