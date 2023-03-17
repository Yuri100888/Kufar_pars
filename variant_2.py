import requests
import sqlite3


class Category():
    '''Класс получающий и хранящий список товаров выбранной категории'''

    def __init__(self):
        self.category_len = 30
        self.catigory_list = []
        self.data_base_list = {}
        self.data_base_list_id = []

    def get_len_category(self, count_url):
        '''находим количество товаров категории в продаже'''
        self.category_len = requests.get(count_url).json()['count']
        print(self.category_len)

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
            self.data_base_list_id.append(str(id[0]))

    def write_to_table(self, name_tab, product):
        '''добавления объявления в базу данных'''
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


class Apartaments(Category):
    count_url = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&prn=1000&size=30&sort=lst.d&typ=sell"

    def __init__(self, message):
        super().__init__()
        self.name_tab = f'apartaments_{message.chat.id}'
        self.url = f"https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&lang=ru&size={self.category_len}&typ=sell"

    def write_to_table(self, name_tab, product):
        super().write_to_table(name_tab, product)


class Product:
    def __init__(self, prod):
        self.product = prod
        self.products_attrs = {}
        self.id = prod['ad_id']
        self.link = prod['ad_link']
        if prod['type'] == 'sell':
            self.deal_type = 'Продажа'       # тип сделки
        else:
            self.deal_type = prod['type']    # это строка на время разработки и теста
        for i in prod['account_parameters']:
            if i['p'] == 'name':             # имя контактного лица
                self.name = i['v']
            elif i['p'] == 'address':        # адрес объекта
                self.address = i['v']

        # определяем название объявления:
        self.name_object = prod['subject']  # название объявления

        if self.product['price_byn'] == '0':
            self.price_byn = 'Договорная'
        else:
            self.price_byn = int(prod['price_byn']) / 100  # цена в рублях
            self.price_usd = int(prod['price_usd']) / 100  # цена в долларах
        # определяем фото:
        try:
            id_images = prod['images'][0]['id']
            pre_id_images = id_images[0:2]
            self.img = f'https://yams.kufar.by/api/v1/kufar-ads/images/{pre_id_images}/{id_images}.jpg?rule=gallery'

        except:
            self.img = 'Фото отсутствует'

    def get_products_attrs(self):
        '''на вход получает аттрибуты объявления в формате json и присваивает их экземпляру класса'''
        self.products_attrs['id'] = self.id      # id объявления
        self.products_attrs['link'] = self.link  # ссылка на объявление
        # определяем тип сделки:
        self.products_attrs['deal_type'] = self.deal_type # тип объявления
        self.products_attrs['name'] = self.name           # контактное лицо
        self.products_attrs['address'] = self.address     # адрес

        # определяем название объявления:
        self.products_attrs['name_object'] = self.name_object  # название объявления
        # определяем цену:
        self.products_attrs['price_byn'] = self.price_byn      # цена
        if self.price_byn != 'Договорная':
            self.products_attrs['price_byn'] = f'{self.price_byn}руб.' # цена в рублях
            self.products_attrs['price_usd'] = f'{self.price_usd}$'    # цена в $



class Apartament(Product):
    def __init__(self, prod):
        super(Apartament, self).__init__(prod)
        for i in prod['ad_parameters']:
            if i['p'] == 'rooms':  # определяем количество комнат
                self.rooms = i['v']
            elif i['p'] == 'size':  # определяем площадь жилья
                self.size = i['v']
            elif i['p'] == 'floor':  # определяем этаж квартиры
                self.floor = i['v']

    def get_products_attrs(self):
        super(Apartament, self).get_products_attrs()
        try:
            self.products_attrs['rooms'] = f'{self.rooms}комн.'
            self.products_attrs['size'] = f'{self.size}м2'
            self.products_attrs['floor'] = f'{self.floor} этаж'
        except Exception:
            print(Exception)

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
# get_list_category(
#     "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=1&typ=sell")
