import telebot
from telebot import types
import time
import requests
from bs4 import BeautifulSoup
import sqlite3

bot = telebot.TeleBot('5108887133:AAHGUwU9cl_NJl-dxmX5hCfly05ICl2OLEA')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'}

categories = {"elektrotransport": {"url": "https://www.kufar.by/l/elektrotransport"}}
user = {'is_working':True}

# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    # Добавляем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Дома и дачи")
    item2 = types.KeyboardButton("Гаражи")
    item3 = types.KeyboardButton("Самокаты")
    markup.add(item1, item2, item3)
    msg = bot.send_message(message.chat.id,
                           '\nНажми: \nДома и дачи - для отслеживания свежих предложений в этой категории\n'
                           'Гаражи — для отслеживания свежих предложений в этой категории\n'
                           'Самокаты - для отслеживания предложений по электротранспорту ',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, change_category)


def change_category(message):
    if message.text.strip() == 'Самокаты':
        get_electrotransport(message, categories['elektrotransport']['url'], 'elektrotransport')


def get_electrotransport(message, url, category):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Стоп")
    markup.add(item1)
    msg = bot.send_message(message.chat.id,
                           f'Отслеживание "{message.text}" началось! \n'
                           'Для остановки отслеживания нажмите "Стоп',
                           reply_markup=markup)
    create_table(f'{category}_{str(message.chat.id)}')
    count = 1
    bot.register_next_step_handler(msg, start)
    while True:
        req = requests.get(url, headers=headers).text
        soup = BeautifulSoup(req, 'html.parser')
        products = soup.find_all(class_="styles_wrapper__IMYdY")
        for i in products:
            idies = get_idies(f'{category}_{str(message.chat.id)}')
            product = {}
            product['id'] = i['href'].split('/')[-1].split('?')[0]
            if product['id'] not in idies:
                product['link'] = i['href']
                img = i.find_next(class_="styles_image__CTXvl lazyload")
                product['img'] = img['data-src']
                product['name'] = img['alt']
                product['price'] = i.find_next(class_="styles_price__tiO8k").text
                write_to_table(f'{category}_{str(message.chat.id)}', product)
                bot.send_message(message.chat.id,
                                 f"{product['img']}\n"
                                 f"{product['name']}\n"
                                 f"{product['price']}\n"
                                 f"{product['link']}\n\n")
            else:
                continue
        print(count)
        count += 1
        time.sleep(60)
        if count % 60 == 0:
            bot.send_message(message.chat.id,
                             f'Цикл выполнен {count} раз')



def create_table(name_table):
    conn = sqlite3.connect('products.db')
    # Создаём курсор:
    cursor = conn.cursor()
    '''создаем таблицу с название по id чата'''
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {name_table}(id INTEGER PRIMARY KEY AUTOINCREMENT, product_id TEXT,
                                    name TEXT, price TEXT,  link TEXT, img TEXT) ''')


def write_to_table(message, product):
    conn = sqlite3.connect('products.db')
    # Создаём курсор:
    cursor = conn.cursor()
    cursor.execute(f'''INSERT INTO {message}(product_id,
                                                            name, price, link, img) VALUES (?,?,?,?,?)''',
                   (product['id'], product['name'], product['price'], product['link'], product['img']))
    conn.commit()


def get_idies(message):
    conn = sqlite3.connect('products.db')
    # Создаём курсор:
    cursor = conn.cursor()
    cursor.execute(f'''SELECT product_id FROM {message}''')
    idies_list = cursor.fetchall()
    idies_list_1 = []
    for id in idies_list:
        idies_list_1.append(id[0])
    return idies_list_1


# Запускаем бота
bot.polling(none_stop=True, interval=0)
