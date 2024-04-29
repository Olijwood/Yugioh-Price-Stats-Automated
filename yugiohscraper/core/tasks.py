from celery import shared_task
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random 

@shared_task
def get_simulated_total_for_qcr_core_set(qcr_core_set_list):
    set_qcr_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Quarter Century']
    set_secret_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Secret Rare']
    set_ultra_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Ultra Rare']
    set_super_prices = [card[1] for card in qcr_core_set_list if card[0] == 'Super Rare']

    # Get random samples of prices for each rarity
    super_total = random.choices(set_super_prices, k=18)
    ultra_total = random.choices(set_ultra_prices, k=4)
    secret_total = random.choices(set_secret_prices, k=2)

    # Determine if the booster box contains a Quarter Century Rare
    if random.randint(1, 4) == 1:
        qcr = random.choice(set_qcr_prices)
        # Replace Ultra or Secret with QCR
        if random.randint(1, 2) == 1:
            ultra_total[-1] = qcr
        else:
            secret_total[-1] = qcr

    # Calculate the total booster value
    total = sum(super_total) + sum(ultra_total) + sum(secret_total)
    return total

@shared_task
def old_get_simulated_total_for_qcr_core_set(qcr_core_set):
    set_qcr = qcr_core_set.filter(card_rarity='Quarter Century')
    set_secret = qcr_core_set.filter(card_rarity='Secret Rare')
    set_ultra = qcr_core_set.filter(card_rarity='Ultra Rare')
    set_super = qcr_core_set.filter(card_rarity='Super Rare')

    set_qcr_prices = [float(qcr.get_market_price()) for qcr in set_qcr]
    set_secret_prices = [float(secret.get_market_price()) for secret in set_secret]
    set_ultra_prices = [float(ultra.get_market_price()) for ultra in set_ultra]
    set_super_prices = [float(super_.get_market_price()) for super_ in set_super]

    # Get random samples of prices for each rarity
    super_total = random.choices(set_super_prices, k=18)
    ultra_total = random.choices(set_ultra_prices, k=4)
    secret_total = random.choices(set_secret_prices, k=2)

    # Determine if the booster box contains a Quarter Century Rare
    if random.randint(1, 4) == 1:
        qcr = random.choice(set_qcr_prices)
        # Replace Ultra or Secret with QCR
        if random.randint(1, 2) == 1:
            ultra_total[-1] = qcr
        else:
            secret_total[-1] = qcr

    # Calculate the total booster value
    total = sum(super_total) + sum(ultra_total) + sum(secret_total)
    return total


@shared_task
def scrape_cards_page(page_url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(page_url)
        wait = WebDriverWait(driver, 40)
        try:
            elements = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, 'search-result')))
            for element in elements:
                wait.until(EC.visibility_of(element))
            print('Page fully loaded')
        except TimeoutException:
            print("Timed out waiting for element to be visible")

        body = driver.find_element(By.TAG_NAME, 'body')
        return body.get_attribute('innerHTML')
    

@shared_task
def scrape_card_detail_page(url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 25)
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.v-lazy-image.v-lazy-image-loaded')))
            print('page fully loaded')
        except TimeoutException:
            print("Timed out waiting for element to be visible")
        body = driver.find_element(By.TAG_NAME, 'body')
        return body.get_attribute('innerHTML')