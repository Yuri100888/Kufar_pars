import telebot
from telebot import types
import variant_2
import main
import time

bot = telebot.TeleBot('5108887133:AAHGUwU9cl_NJl-dxmX5hCfly05ICl2OLEA')
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/108.0.0.0 YaBrowser/23.1.1.1138 Yowser/2.5 Safari/537.36'}

# Команда start
@bot.message_handler(commands=["start"])
def start(message):
    # Добавляем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Дома и дачи")
    item2 = types.KeyboardButton("Гаражи")
    item3 = types.KeyboardButton("Самокаты")
    item4 = types.KeyboardButton("Квартиры")
    markup.add(item1, item2, item4, item3)
    msg = bot.send_message(message.chat.id,
                           '\nНажми: \nДома и дачи - для отслеживания свежих предложений в этой категории\n'
                           'Гаражи — для отслеживания свежих предложений в этой категории\n'
                           'Самокаты - для отслеживания предложений по электротранспорту ',
                           reply_markup=markup)
    bot.register_next_step_handler(msg, operation)

def operation(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("Стоп")
    markup.add(item1)
    msg = bot.send_message(message.chat.id,
                           f'Отслеживвание категории "{message.text.strip()}" началось',
                           reply_markup=markup)
    if message.text.strip() == 'Квартиры':
        obj = variant_2.Apartaments(message) # создали объект "Квартиры"
        obj.get_len_category(obj.count_url) # получили количество квартир в продаже
        obj.get_list_category(obj.url) # получили список квартир в продаже
        obj.create_table(obj.name_tab) # создаём таблицу
        for o in obj.page['ads']:
            obj.get_data_base_list(obj.name_tab) # получаем список квартир в базе
            apart = variant_2.Apartament(o) # создаём продукт как отдельный продукт
            apart.get_products_attrs()
            # print(obj.data_base_list)
            print(apart.id)
            if str(apart.id) not in obj.data_base_list_id:
                print(obj.data_base_list_id)
                obj.write_to_table(obj.name_tab, apart)
                bot.send_message(message.chat.id,
                                     f"{apart.img}\n"
                                     f"{apart.name_object}\n"
                                     f"{apart.address}\n"
                                     f"{apart.rooms} комн.\n"
                                     f"{apart.size}м2\n"
                                     f"{apart.floor} этаж\n"
                                     f"{apart.price_byn}руб.\n"
                                     f"{apart.price_usd}$\n"
                                     f"{apart.link}\n\n"
                                 )

            else:
                continue
    bot.register_next_step_handler(msg, start)

# Запускаем бота
bot.polling(none_stop=True, interval=0)