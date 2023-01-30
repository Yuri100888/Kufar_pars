import requests
from pprint import pprint
from bs4 import BeautifulSoup


'''это файл для проб'''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'}
# получение списка объявлений
# page = requests.get("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=10&typ=sell")
# page_2 = requests.get("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=30&typ=sell")
# page_3 = requests.get("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=30&typ=sell")
# p = requests.get("https://content.kufar.by/static/kufar-fe-realty/_next/static/chunks/pages/listings-7d7c132d26e0f3f1.js")
# print(p.content)
# pprint(page.json())
# самокаты https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=4160&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D&lang=ru&size=43
# url_1 = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=4160&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D&lang=ru&size=1"
url_1 = "https://www.kufar.by/l/elektrotransport"

r = requests.get(url_1, headers=headers).text
soup = BeautifulSoup(r, 'html.parser')
re = soup.find_all(class_='styles_content__right__ddauo')
re1 = soup.find_all('img')
re2 = soup.find_all(class_="styles_wrapper__IMYdY")

for i in re2:
    product = {}
    product['link'] = i['href']
    product['id'] = i['href'].split('/')[-1].split('?')[0]
    img = i.find_next(class_="styles_image__CTXvl lazyload")
    product['img'] = img['data-src']
    product['name'] = img['alt']
    product['price']=i.find_next(class_="styles_price__tiO8k").text
    print(f"{product}\n\n")
# print(re)
# print(len(re2))
# user_data = {"us_id": "",
#              "is_working": False,
#              "category_count_url": "",
#              "category_url": '',
#              "coun": 0}
