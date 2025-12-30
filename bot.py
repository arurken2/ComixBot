import telebot
from telebot import types
import random
import os

# Получаем токен из переменной окружения
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Список пользователей, получивших открытку
used_users = set()

# Словарь с открытками и текстами
cards = {
    1: {'image': 'images/Cleopatra.png', 'text': 'тебе должна была дарить подарок начальница Клеопатра Михайловна, но... она, конечно, не забыла! просто как раз планировала отдать свой отпуск на Пхукете тебе за хорошую работу! \n с 2026 годом, счастливчик!!!'},
    2: {'image': 'images/Edic.png', 'text': 'твое имя выпало Эдику — победа? он сделал подарок своими руками, и это очень мило, но... стоп, почему у него нож?.. \n в любом случае, с наступающим 2026 годом!'},
    3: {'image': 'images/Evgeny.png', 'text': 'твое имя выпало так называемому Евгению-бухгалтеру! но не торопись радоваться, его предпочтения немного специфичны... он выбрал тебе новогодний набор шоколада «Бабаевский» и стал единственным его покупателем за год. но он очень старался. \n в любом случае, с наступающим 2026 годом!'},
    4: {'image': 'images/Jana.png', 'text': 'твое имя выпало Яне-эйчарке — джекпот! подарок по твоей эстетке, собранный по цветам, а еще самодельная открытка. она готовила его всю неделю и очень ждет твоей реакции! \n юху, с наступающим 2026 годом!'},
    5: {'image': 'images/Twins.png', 'text': 'тебе дарят подарки близнецы-рыжики Леха и Сашок. возможно, у тебя самый веселый подарок в офисе. Возможно, придется передарить его своему племяшке... \n в любом случае, с наступающим 2026 годом!'}
}

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    
    if user_id in used_users:
        return
    
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton('Узнать (только бы Эдмэн!!!)', callback_data='get_card')
    markup.add(button)
    
    bot.send_message(message.chat.id, 'ура, последний рабочий день завершается офисным сантой! \n \n Узнавай, кто из коллег дарит тебе подарок!' , reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'get_card')
def send_card(call):
    user_id = call.from_user.id
    
    if user_id in used_users:
        return
    
    card_id = random.randint(1, 5)
    card_data = cards[card_id]
    
    with open(card_data['image'], 'rb') as photo:
        bot.send_photo(call.message.chat.id, photo, caption=card_data['text'])
    
    used_users.add(user_id)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)

# Запуск бота
print('Bot started...')
bot.polling(none_stop=True)