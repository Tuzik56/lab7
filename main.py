import telebot
from telebot import types
from functional import timetable_day, timetable_week, week_day, week_parity

token = "5923069219:AAG3H9zA7sZr2boX3cyyUgGxpm49G29i7U0"
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def command_start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Расписание", "/help")
    bot.send_message(message.chat.id, 'Здравствуйте, это бот с расписанием для группы БВТ2204 МТУСИ.',
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def command_help(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Расписание")
    bot.send_message(message.chat.id, 'Я умею:\n/help - узнать информация обо мне\n/mtuci - перейти на сайт '
                                       'МТУСИ\n/week - узнать четность недели\nРасписание - узнать расписание '
                                       'на:\nСегодня\nЗавтра\nТекущую неделю\nСледующую неделю', reply_markup=keyboard)


@bot.message_handler(commands=['week'])
def command_week(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Расписание", "/help")
    bot.send_message(message.chat.id, f"Сейчас {week_parity('today', False).lower()}", reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def command_mtuci(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Расписание", "/help")
    bot.send_message(message.chat.id, 'Ссылка на сайт нашего вуза - https://mtuci.ru/', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def command_text(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    message_text = message.text.lower()

    if message_text == 'расписание':
        keyboard.add('Сегодня', 'Завтра', 'Текущая неделя', 'Следующая неделя', '/help')
        bot.send_message(message.chat.id, 'Выберите день', reply_markup=keyboard)

    elif message_text == 'сегодня':
        keyboard.row("Расписание", "/help")
        bot.send_message(message.chat.id, timetable_day(week_day('today'), week_parity('today', False)),
                         reply_markup=keyboard)

    elif message_text == 'завтра':
        keyboard.row("Расписание", "/help")
        bot.send_message(message.chat.id, timetable_day(week_day('tomorrow'), week_parity('tomorrow', False)),
                         reply_markup=keyboard)

    elif message_text == "текущая неделя":
        keyboard.row("Расписание", "/help")
        bot.send_message(message.chat.id, timetable_week(week_parity('today', False)), reply_markup=keyboard)

    elif message_text == "следующая неделя":
        keyboard.row("Расписание", "/help")
        bot.send_message(message.chat.id, timetable_week(week_parity('today', True)), reply_markup=keyboard)
    else:
        keyboard.row("Расписание", "/help")
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.polling(none_stop=True)
