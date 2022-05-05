# Gizem Yıldırım
import pandas as pd
import requests
from bs4 import BeautifulSoup

# categories

categories = (
    ['atistirmalik','ev-bakim-temizlik', 'icecek', 'kahvaltilik-sut-urunleri',
    'ambalaj-malzemeleri','hazir-yemek','meyve-sebze','et-tavuk-balik',
     'saglikli-yasam-urunleri','temel-gida']
)

category_names = ['Atıştırmalık', 'Ev Bakım & Temizlik', 'İçecek', 'Kahvaltılık & Süt Ürünleri',
                 'Ambalaj Malzemeleri','Hazır Yemek','Meyve & Sebze', 'Et & Tavuk & Balık', 
                  'Sağlıklı Yaşam Ürünleri', 'Temel Gıda']

category_dictionary = {k:v for k,v in zip(categories,category_names)}

# getting responses for different categories

url = "https://www.a101.com.tr/market/"
responses = pd.DataFrame()
category_ = []
response_ = []

for category in category_dictionary.keys():
    url_ = url + str(category) + '/'
    for page_number in range(1,25):
        response = requests.get(url_ + '?page=' + str(page_number))
        category_.append(category_dictionary.get(category))
        response_.append(response)
        
responses['category'] = category_
responses['response'] = response_

name = "article"
class_name = "product-card js-product-wrapper"

# getting item info for each categories in different pages

item_prices = []

for category in category_dictionary.values():
    #print(category)
    temp_df = responses[responses['category'] == category]
    
    for response in temp_df['response']:
        soup = BeautifulSoup(response.text)
        name = "article"
        class_name = "product-card js-product-wrapper"

        item_list = soup.find_all(name, {"class": class_name})

        for item in item_list:
            price = float(item.find("span", {"class": "current"}).text[1:].strip().replace(",","."))
            item_name = item.find("h3", {"class": "name"}).text.strip()
            item_prices.append([item_name, category, price]) 

item_df = pd.DataFrame(item_prices, columns=['Product Name', 'Subcategory', 'Price'])
print('Web scraping is complete!')
        
