import requests
import sqlite3


class Category():
    '''Класс получающий и хранящий список товаров выбранной категории'''
    def __init__(self):
        self.category_len = 1
        self.catigory_list = {}
        self.data_base_list = {}

    def get_len_category(self, count_url):
        '''находим количество товаров категории в продаже'''
        self.category_len = requests.get(count_url).json()['count']

    def get_list_category(self, url):
        '''находим все товары (словарь товаров), имеющиеся в продаже '''
        self.page = requests.get(url).json()

    def create_table(self, name_tab):
        '''создаём таблицу для хранения товаров с их аттрибутами'''
        conn = sqlite3.connect('products.db')
        # Создаём курсор:
        cursor = conn.cursor()
        '''создаем таблицу с название по id чата'''
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name_tab}(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id TEXT,
                                    name TEXT, link TEXT, address TEXT, price_byn INEGER, price_usd INTEGER, deal_type TEXT) ''')

    def get_data_base_list(self, name_tab):
        '''находим все товары категории из базы (их id и стоимость)'''
        conn = sqlite3.connect('products.db')
        # Создаём курсор:
        cursor = conn.cursor()
        cursor.execute(f'''SELECT product_id, price_byn FROM {name_tab}''')
        base_list = cursor.fetchall()
        # ____________________________
        for id in base_list:
            self.data_base_list[id[0]] = id[1]

    def write_to_table(self, name_tab, product):
        conn = sqlite3.connect('products.db')
        # Создаём курсор:
        cursor = conn.cursor()
        try:
            cursor.execute(f'''INSERT INTO {name_tab}(product_id,
                                                                name, link, address, price_byn, price_usd, deal_type) VALUES (?,?,?,?,?,?,?)''',
                           (
                               product.products_attrs["id"], product.products_attrs["name"],
                               product.products_attrs["link"],
                               product.products_attrs["address"], product.products_attrs["price_byn"],
                               product.products_attrs["price_usd"], product.products_attrs["deal_type"]
                           )
                           )
        except KeyError:
            cursor.execute(f'''INSERT INTO {name_tab}(product_id,
                                                                            name, link, address, price_byn, deal_type) VALUES (?,?,?,?,?,?)''',
                           (
                               product.products_attrs["id"], product.products_attrs["name"],
                               product.products_attrs["link"],
                               product.products_attrs["address"], product.products_attrs["price_byn"],
                               product.products_attrs["deal_type"]
                           )
                           )
        conn.commit()

class Houses(Category):
    count_url = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&size=30&typ=sell"
    def __init__(self, messagge):
        self.name_tab = f'{messagge.chat.id}_houses'
        self.url  = f"https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size={self.category_len}&typ=sell"
        super().__init__()

    def write_to_table(self,name_tab, product):
        super().write_to_table(name_tab, product)


class Product:
    def __init__(self, prod):
        self.product = prod
        products_attrs = {}

        def get_products_attrs(self, attrs):
            '''на вход получает аттрибуты объявления в формате json и присваивает их екземпляру класса'''
            self.products_attrs['id'] = attrs['ad_id']
            self.products_attrs['link'] = attrs['ad_link']
            # self.id = attrs['ad_id']
            # self.link = attrs['ad_link']
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
                self.products_attrs[
                    'images'] = f'https://yams.kufar.by/api/v1/kufar-ads/images/{pre_id_images}/{id_images}.jpg?rule=gallery'

            except:
                self.products_attrs['images'] = 'Фото отсутствует'



        # _____________________________Пробы
# a = Houses(me)
# a.get_len_category(a.count_url)

data_base_list = {}
def get_data_base_list(name_tab):
    conn = sqlite3.connect('products.db')
    # Создаём курсор:
    cursor = conn.cursor()
    cursor.execute(f'''SELECT product_id, price_byn FROM {name_tab}''')
    base_of_products_list = cursor.fetchall()
    for prod in base_of_products_list:
        data_base_list[prod[0]] = prod[1]
    print(data_base_list)
def get_list_category(url):
        '''находим все товары (словарь товаров), имеющиеся в продаже '''
        page = requests.get(url).json()
        print(page)


# get_data_base_list("tab_1353621251")
get_list_category("https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=1&typ=sell")