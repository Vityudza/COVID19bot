import COVID19Py
from telebot import types
import telebot

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('1028374464:AAFIi0dXN9EiRwXBk6MqpSmteAvJvXH725g')



@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('В усьому світі')
    btn2 = types.KeyboardButton('Україна')
    btn3 = types.KeyboardButton('США')
    btn4 = types.KeyboardButton('Росія')
    markup.add(btn1, btn2, btn3, btn4)

    send_message = f"<b>Привіт {message.from_user.first_name}!</b>\nВведіть країну"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def mess(message):
    final_message = ""
    get_message_bot = message.text.strip().lower()
    if get_message_bot == "україна":
        location = covid19.getLocationByCountryCode("UA")
    elif get_message_bot == "сша":
        location = covid19.getLocationByCountryCode("US")
    elif get_message_bot == "росія":
        location = covid19.getLocationByCountryCode("RU")
    else:
        location = covid19.getLatest()
        final_message = f"<u>Ситуація в світі:</u>\n<b>Захворілих: </b>{location['confirmed']:,}\n<b>Смертей: </b>{location['deaths']:,}"

    if final_message == "":
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = f"<u>Відомості про країну:</u>\nНаселення: {location[0]['country_population']:,}\n" \
            f"Останнє оновлення: {date[0]} {time[0]}\nОстанні відомості:\n<b>" \
            f"Захворілих: </b>{location[0]['latest']['confirmed']:,}\n <b>Смертей: </b>" \
            f"{location[0]['latest']['deaths']:,}"


    bot.send_message(message.chat.id, final_message, parse_mode='html')

bot.polling(none_stop=True)