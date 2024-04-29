from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from bs4 import BeautifulSoup
import os

def scrape_yugioh_sets(url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'magicSets')))
            html = driver.page_source
        except TimeoutException:
            print("Timed out waiting for element to be visible")
            return None

    soup = BeautifulSoup(html, 'html.parser')
    print('scraped html soup')
    return soup

def old_scrape_yugioh_sets(url=None):
    url = 'https://shop.tcgplayer.com/yugioh?newSearch=true&_gl=1*a98xor*_gcl_au*MzcyOTUwOTU3LjE3MTA5MjM5MzA.*_ga*MTk3NTI4NjUyMy4xNzEwOTIzOTMw*_ga_VS9BE2Z3GY*MTcxMTM2NjE0My4zLjAuMTcxMTM2NjE0My42MC4wLjA.'
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    print('starting to scrape')
    html = ''
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(url)
        print('opened page')
        wait = WebDriverWait(driver, 15)
        try:
            element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'magicSets')))
            print('page fully loaded')
            html = driver.page_source
        except TimeoutException:
            print("Timed out waiting for element to be visible")
    print('HTML ready')
    return html

def old_scrape_cards_page(page_url, options):
    retry_attempts = 3
    while retry_attempts > 0:
        try:
            with webdriver.Chrome(options=options) as driver:
                driver.get(page_url)
                # time.sleep(6)
                wait = WebDriverWait(driver, 15)
                try:
                    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.v-lazy-image.v-lazy-image-loaded')))
                    print('page fully loaded')
                except TimeoutException:
                    print("Timed out waiting for element to be visible")
                body = driver.find_element(By.TAG_NAME, 'body')
                print('scraped page of set')
                return body.get_attribute('innerHTML')
        except ConnectionError as e:
            print(f"ConnectionError occurred: {e}")
            print("Retrying...")
            time.sleep(5)
            retry_attempts -= 1

def scrape_cards_page(page_url):
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    with webdriver.Chrome(options=chrome_options) as driver:
        driver.get(page_url)
        wait = WebDriverWait(driver, 15)
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.v-lazy-image.v-lazy-image-loaded')))
            print('Page fully loaded')
        except TimeoutException:
            print("Timed out waiting for element to be visible")

        body = driver.find_element(By.TAG_NAME, 'body')
        return body.get_attribute('innerHTML')
