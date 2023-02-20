'''Пробую сделать код через ООП и библотеку request'''
import requests
import sqlite3

# Создаём БД:
conn = sqlite3.connect('products.db')
# Создаём курсор:
cursor = conn.cursor()


class Page():
    '''этот класс создает страницу с объявлениями'''

    def __init__(self):
        self.page = ''
        self.count = 1

    def get_count(self, url_count):
        '''получаем количество подходящих объявлений'''
        self.count = requests.get(url_count).json()['count']

    def get_houses(self):
        '''получаем список объявлений в формате jcon'''
        self.page = requests.get(
            f"https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size={self.count}&typ=sell").json()

    def get_apartments(self):
        self.page = requests.get(
            f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&lang=ru&size={self.count}&typ=sell').json()

    def get_garages(self):
        '''получаем список объявлений в формате jcon'''
        self.page = requests.get(
            f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1030&cur=BYR&gbx=b%3A28.549494959716743%2C55.49950816218998%2C28.709140040283156%2C55.60771349172756&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&lang=ru&size={self.count}&typ=sell').json()

    def get_elektrotransport(self):
        '''получаем список объявлений в формате jcon'''
        self.page = requests.get(
            f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=4160&cursor=eyJ0IjoiYWJzIiwiZiI6dHJ1ZSwicCI6M30%3D&lang=ru&&size={self.count}').json()


class Product():
    '''этот класс получает все аттрибуты объявления'''

    def __init__(self):
        self.products_attrs = {}

        # self.phone = phone

    def get_products_attrs(self, attrs):
        '''на вход получает аттрибуты объявления в формате json и присваивает их екземпляру класса'''
        self.products_attrs['id']=attrs['ad_id']
        self.products_attrs['link']=attrs['ad_link']
        #self.id = attrs['ad_id']
        #self.link = attrs['ad_link']
        # определяем тип сделки:
        if attrs['type'] == 'sell':
            self.products_attrs['deal_type'] = 'Продажа'
        else:
            print(attrs['type'])  # это строка на время разработки и теста
        for i in attrs['account_parameters']:
            if i['p'] == 'name':
                self.products_attrs['name'] = i['v']
            elif i['p'] == 'address':
                self.products_attrs['address'] = i['v']

        # определяем название объявления:
        self.products_attrs['name_object'] = attrs['subject']

        # определяем цену:
        if attrs['price_byn'] == '0':
            self.products_attrs['price_byn'] = 'Договорная'
        else:
            self.products_attrs['price_byn'] = int(attrs['price_byn']) / 100
            self.products_attrs['price_usd'] = int(attrs['price_usd']) / 100
        # определяем фото:
        try:
            id_images = attrs['images'][0]['id']
            pre_id_images = id_images[0:2]
            self.products_attrs['images'] = f'https://yams.kufar.by/api/v1/kufar-ads/images/{pre_id_images}/{id_images}.jpg?rule=gallery'

        except:
            self.products_attrs['images'] = 'Фото отсутствует'
            # определяем телефон:
            # get_phone = \
            # requests.get(f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/item/161719993/phone')
            # self.phone=get_phone
            # выдает ошибку "response 400"


class Operator():

    def __init__(self, chat_id, category_count, category_url):
        self.products_page = Page()
        self.chat_id = f'tab_{chat_id}'
        self.answer = []
        self.category_count = category_count
        self.category_url = category_url

    def get_products(self):
        '''получаем список всех продуктов категории'''
        self.products_page.get_count(self.category_count)
        if self.category_url == 'garages':
            self.products_page.get_garages()
        elif self.category_url == 'houses':
            self.products_page.get_houses()
        elif self.category_url == "elektrotransport":
            self.products_page.get_elektrotransport()
        elif self.category_url == 'apartaments':
            self.products_page.get_apartments()

    def create_table(self):
        conn = sqlite3.connect('products.db')
        # Создаём курсор:
        cursor = conn.cursor()
        '''создаем таблицу с название по id чата'''
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.chat_id}(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id TEXT,
                                    name TEXT, link TEXT, address TEXT, price_byn INEGER, price_usd INTEGER, deal_type TEXT) ''')

    def write_to_table(self, product):
        conn = sqlite3.connect('products.db')
        # Создаём курсор:
        cursor = conn.cursor()
        try:
            cursor.execute(f'''INSERT INTO {self.chat_id}(product_id,
                                                                name, link, address, price_byn, price_usd, deal_type) VALUES (?,?,?,?,?,?,?)''',
                           (
                               product.products_attrs["id"], product.products_attrs["name"], product.products_attrs["link"],
                               product.products_attrs["address"], product.products_attrs["price_byn"],
                               product.products_attrs["price_usd"], product.products_attrs["deal_type"]))
        except KeyError:
            cursor.execute(f'''INSERT INTO {self.chat_id}(product_id,
                                                                            name, link, address, price_byn, deal_type) VALUES (?,?,?,?,?,?)''',
                           (
                               product.products_attrs["id"], product.products_attrs["name"],
                               product.products_attrs["link"],
                               product.products_attrs["address"], product.products_attrs["price_byn"],
                               product.products_attrs["deal_type"]))
        conn.commit()

    def get_idies(self):
        conn = sqlite3.connect('products.db')
        # Создаём курсор:
        cursor = conn.cursor()
        cursor.execute(f'''SELECT product_id FROM {self.chat_id}''')
        idies_list = cursor.fetchall()
        idies_list_1 = []
        for id in idies_list:
            idies_list_1.append(int(id[0]))
        return idies_list_1

# --------------TEST----------------------
