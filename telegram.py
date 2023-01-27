import telebot
from telebot import types
import main
import time

# гаражи:
# garages = f'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1030&cur=BYR&gbx=b%3A28.549494959716743%2C55.49950816218998%2C28.709140040283156%2C55.60771349172756&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&lang=ru&size={self.count}&typ=sell'
count_garages = 'https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1030&cur=BYR&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&prn=1000&size=30&sort=lst.d&typ=sell'

# дома и дачи:
# house = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size=30&typ=sell"
house = 'f"https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size={self.count}&typ=sell"'
count_house = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&size=30&typ=sell"
# Самокаты:
count_elektrotransport = "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=4160"


# Создаем бота
bot = telebot.TeleBot('5108887133:AAHGUwU9cl_NJl-dxmX5hCfly05ICl2OLEA')


class User():
    def __init__(self, us_id):
        self.us_id = us_id
        self.is_working = False
        self.category_count_url = ''
        self.category_url = ''
        self.coun = 0

    def stop_working(self):
        self.is_working = False

    def get_category_count_url(self, count_url):
        '''получаем количество подходящих объявлений'''
        # count_product = requests.get(
        #        "https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&size=30&typ=sell")
        # count_product=requests.get(count_url)
        # self.count = count_product.json()['count']
        self.category_count_url = count_url

    def get_categoty_url(self, url):
        '''получаем список объявлений в формате jcon'''
        # self.page = requests.get(
        #     f"https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1010&cur=USD&gtsy=country-belarus~province-vitebskaja_oblast&lang=ru&size={self.count}&typ=sell").json()
        self.category_url = url


# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    global user
    user = User(message.chat.id)

    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Дома и дачи")
    item2 = types.KeyboardButton("Гаражи")
    item3 = types.KeyboardButton("Самокаты")
    markup.add(item1, item2, item3)
    user.is_working = True
    # types.ReplyKeyboardRemove(selective=False)

    # markup = telebot.types.InlineKeyboardMarkup()
    # markup.add(telebot.types.InlineKeyboardButton(text='Дома и дачи', callback_data='Дома и дачи'))
    # markup.add(telebot.types.InlineKeyboardButton(text='Гаражи', callback_data='Гаражи'))

    msg = bot.send_message(message.chat.id, '\nНажми: \nДома и дачи - для отслеживания свежих предложений в этой категории\n'
                                      'Гаражи — для отслеживания свежих предложений в этой категории\n'
                                            'Самокаты - для отслеживания предложений по электротранспорту ',
                     reply_markup=markup)
    bot.register_next_step_handler(msg, handle_text)


@bot.message_handler(commands=["stop" or "Стоп"])
def stop(message, res=False):
    user.stop_working()
    # bot.send_message(m.chat.id, 'Бот будет остановлен\n!!!')
    bot.send_message(message.chat.id,
                     f'{message.chat.first_name}, отслеживание категории "{message.text}" остановленно!\n'
                     f'Для настройки и запуска бота нажмите здесь "/start" или введите команду start')

    bot.register_next_step_handler(message, start)


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global user

    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup1.add(types.KeyboardButton('/stop'))
    bot.register_next_step_handler(message, operation)
    if message.text.strip() == 'Дома и дачи':
        # bot.send_message(message.chat.id, 'Будем отслеживать дома и дачи', reply_markup=markup1)
        user.get_category_count_url(count_house)
        user.category_url = 'houses'
        user.is_working = True
        msg = bot.send_message(message.chat.id, "Для подтверждения отправьте '1'", reply_markup=markup1)


        # bot.register_next_step_handler(message, operation)


    elif message.text.strip() == 'Гаражи':
        # bot.register_next_step_handler(message, callback=operation)
        # bot.send_message(message.chat.id, 'Будем отслеживать гаражи', reply_markup=markup1)
        user.get_category_count_url(count_garages)
        user.category_url = 'garages'
        user.is_working = True
        msg = bot.send_message(message.chat.id, "Для подтверждения отправьте '1'", reply_markup=markup1)

    elif message.text.strip() == 'Самокаты':
        # bot.register_next_step_handler(message, callback=operation)
        # bot.send_message(message.chat.id, 'Будем отслеживать гаражи', reply_markup=markup1)
        user.get_category_count_url(count_elektrotransport)
        user.category_url = 'elektrotransport'
        user.is_working = True
        msg = bot.send_message(message.chat.id, "Для подтверждения отправьте '1'", reply_markup=markup1)


def operation(message):
    msg_oper = bot.send_message(message.chat.id, "Отслеживание началось")
    while user.is_working == True:

        a = main.Operator(message.chat.id, user.category_count_url, user.category_url)
        a.get_products()
        a.create_table()
        for attrs in a.products_page.page['ads']:
            if user.is_working == True:
                product = main.Product()
                product.get_products_attrs(attrs)
                if product.id not in a.get_idies():
                    a.write_to_table(product)
                    if product.price_byn == 'Договорная':
                        bot.send_message(message.chat.id,
                                         f'{product.images}\n{product.link}\n{product.address}\n{product.price_byn}')
                    else:
                        bot.send_message(message.chat.id,
                                         f'{product.images}\n{product.link}\n{product.address}\n{product.price_byn} руб.\n{product.price_usd}$')
        user.coun += 1
        print(user.coun)
        time.sleep(60)
        if user.coun % 60 == 0:
            bot.send_message(message.chat.id,
                                    f'Цикл выполнен {user.coun} раз')
        bot.register_next_step_handler(msg_oper, start)


# https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1030&cur=BYR&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&lang=ru&size=30&typ=sell
# https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1030&cur=BYR&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&size=30&typ=sell

# гаражи:  https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/rendered-paginated?cat=1030&cur=BYR&gbx=b%3A28.549494959716743%2C55.49950816218998%2C28.709140040283156%2C55.60771349172756&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&lang=ru&size=30&typ=sell
# count гаражи: https://cre-api-v2.kufar.by/items-search/v1/engine/v1/search/count?cat=1030&cur=BYR&gtsy=country-belarus~province-vitebskaja_oblast~locality-novopolock&prn=1000&size=30&sort=lst.d&typ=sell



# Запускаем бота
bot.polling(none_stop=True, interval=0)
