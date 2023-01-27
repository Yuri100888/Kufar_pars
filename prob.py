import requests
from pprint import pprint

'''это файл для проб'''

# получение списка объявлений
# page = requests.get("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=10&typ=sell")
# page_2 = requests.get("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=30&typ=sell")
# page_3 = requests.get("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6Mn0%3D&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=30&typ=sell")
# p = requests.get("https://content.kufar.by/static/kufar-fe-realty/_next/static/chunks/pages/listings-7d7c132d26e0f3f1.js")
# print(p.content)
# pprint(page.json())
#самокаты https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=4160&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D&lang=ru&size=43
url_1 = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=4160&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D&lang=ru&size=1"
#url_1 = "https://www.kufar.by/l/elektrotransport"
# count = 0
# x = True
# while x==True:
#     count+=1
#     print(count)
#     if count == 2:
#         print('стоп')
#         x = False
r = requests.get(url_1)
pprint(r.json())

user_data = {"us_id" : "",
        "is_working" : False,
        "category_count_url" : "",
        "category_url" : '',
        "coun" : 0}