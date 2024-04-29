# short_page_urls = ['/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=1', '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=2', '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=3', '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=4', '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=5', '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=24']
# set_url_no_page = 'https://www.tcgplayer.com' + str('='.join(short_page_urls[0].split('=')[:-1]) + '=')
# print(set_url_no_page)
# last_page_num = int(short_page_urls[-1].split('=')[-1])
# print(last_page_num)
# page_urls = []
# page_num = 1
# while page_num <= last_page_num:
#     page_urls.append(str(set_url_no_page + str(page_num)))
#     page_num += 1
# print(page_urls)

# Sample short_page_urls list
short_page_urls = [
    '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=1',
    '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=2',
    '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=3',
    '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=4',
    '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=5',
    '/search/yugioh/25th-anniversary-rarity-collection?view=grid&productLineName=yugioh&setName=25th-anniversary-rarity-collection&page=24'
]

# Get the base URL without the page number
set_url_no_page = 'https://www.tcgplayer.com' + '='.join(short_page_urls[0].split('=')[:-1])

# Extract the last page number from the last URL
last_page_num = int(short_page_urls[-1].split('=')[-1])

# Generate the list of all page URLs
page_urls = [f"{set_url_no_page}{page_num}" for page_num in range(1, last_page_num + 1)]

print(page_urls)
