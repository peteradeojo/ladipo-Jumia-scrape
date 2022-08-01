import requests
from bs4 import BeautifulSoup
import pandas as pd

"""
Scraping jumia (an E-commerce site) for samsung phones 
"""

# get the url for the site
base_url = "https://www.jumia.com.ng/"

# create an empty list to store the link of each product so we can get all information we need
productlinks = []


for x in range(1, 50):
    r = requests.get(f"https://www.jumia.com.ng/catalog/?q=samsung+phones&page={x}#catalog-listing")
    soup = BeautifulSoup(r.content, 'lxml')
    productlist = soup.find_all('article', class_ = 'prd _fb col c-prd')

    for item in productlist:
        for link in item.find_all('a', href = True):
            productlinks.append(base_url + link['href'])
            
            
samsung_phones = []
for link in productlinks:
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'lxml')
    try:
        name = soup.find('h1', class_ = '-fs20 -pts -pbxs').text
    except:
        name = 'NAN'
    try:
        price = soup.find('span', class_='-b -ltr -tal -fs24').text
    except:
        price = 'NAN'
    try:
        rating = soup.find('div', class_ = 'stars _s _al').text
    except:
        rating = 'NAN'
    try:
        reviews = soup.find('a', class_ = '-plxs _more').text
    except:
        reviews = 'NAN'

    phones = {
        'url': link,
        'name': name,
        'price' : price,
        'rating' : rating,
        'reviews' : reviews
    }

    samsung_phones.append(phones)
    print(f"Saving {phones['name']}")

df = pd.DataFrame(samsung_phones)
print(df.head(15))
