import telebot
from telebot import types
import random

import settings

# Создаем экземпляр бота
bot = telebot.TeleBot(settings.mamin_key)

# Database of gay users
gay_users = ["telegram", "ZhenaKorov"]
predlozka = []
removed_gays = []

@bot.message_handler(commands=['start'])
def start(message):
    # Create buttons
    gay_button = types.KeyboardButton(text="Найти гея")
    offer_gay_button = types.KeyboardButton(text="Предложить гея")
    not_found_button = types.KeyboardButton(text="Такого аккаунта нету")

    # Create keyboard
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(gay_button, offer_gay_button)
    keyboard.row(not_found_button)

    # Send a welcome message with the keyboard to the user
    bot.send_message(message.chat.id, "Привет! Я бот с большой библиотекой геев! Здесь ты можешь найти лоха который стал геем и написать ему в лс.", reply_markup=keyboard)

    # Add the user to the database, excluding certain usernames
    if message.from_user.username not in gay_users and message.from_user.username not in ["TYATYAPKA_FUN", "NE_RESHETO"]:
        gay_users.append(message.from_user.username)

@bot.message_handler(func=lambda message: message.text == "Найти гея")
def find_gay(message):
    if gay_users:
        # Get a random user from the database
        random_gay = random.choice(gay_users)
        bot.send_message(message.chat.id, f"Вот случайный гей: @{random_gay}")
    else:
        bot.send_message(message.chat.id, "В базе данных нет геев. Скоро мы это исправим!")

@bot.message_handler(func=lambda message: message.text == "Предложить гея")
def offer_gay(message):
    cancel_button = types.KeyboardButton(text="Отмена")

    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(cancel_button)

    bot.send_message(message.chat.id, "Напишите @гея, которого хотите предложить:", reply_markup=keyboard)
    bot.register_next_step_handler(message, process_gay_offer)

def process_gay_offer(message):
    if message.text == "Отмена":
        start(message)
        return

    gay_offer = message.text[1:]  # Remove the '@' symbol from the username
    predlozka.append(gay_offer)
    bot.send_message(message.chat.id, f"Гей @{gay_offer} предложен. Спасибо!")

@bot.message_handler(func=lambda message: message.text == "Такого аккаунта нету")
def not_found(message):
    cancel_button = types.KeyboardButton(text="Отмена")

    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row(cancel_button)

    bot.send_message(message.chat.id, "Напишите @гея, которого нужно удалить:", reply_markup=keyboard)
    bot.register_next_step_handler(message, process_gay_not_found)

def process_gay_not_found(message):
    if message.text == "Отмена":
        start(message)
        return

    gay_not_found = message.text[1:]  # Remove the '@' symbol from the username
    removed_gays.append(gay_not_found)
    bot.send_message(message.chat.id, f"Гей @{gay_not_found} предложен на удаление. Спасибо!")

@bot.message_handler(commands=['checkpredlozka'])
def check_predlozka(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        if predlozka:
            offer_list = "\n".join(predlozka)
            bot.send_message(message.chat.id, f"Список предложенных геев:\n{offer_list}")
        else:
            bot.send_message(message.chat.id, "Список предложенных геев пуст.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

@bot.message_handler(commands=['fullbase'])
def full_base(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        if gay_users:
            base = "\n".join(gay_users)
            bot.send_message(message.chat.id, f"База пользователей-геев:\n{base}")
        else:
            bot.send_message(message.chat.id, "База данных пуста.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

@bot.message_handler(commands=['removegay'])
def remove_gay(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        # Split the command into arguments
        command_args = message.text.split()
        if len(command_args) > 1:
            # Get the gay user to remove
            gay_to_remove = command_args[1]
            if gay_to_remove in gay_users:
                gay_users.remove(gay_to_remove)
                removed_gays.append(gay_to_remove)
                bot.send_message(message.chat.id, f"Гей @{gay_to_remove} удален из базы данных.")
            else:
                bot.send_message(message.chat.id, f"Гей @{gay_to_remove} не найден в базе данных.")
        else:
            bot.send_message(message.chat.id, "Укажите гея, которого нужно удалить.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

@bot.message_handler(commands=['addgay'])
def add_gay(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        # Split the command into arguments
        command_args = message.text.split()
        if len(command_args) > 1:
            # Get the gay user to add
            gay_to_add = command_args[1]
            if gay_to_add not in gay_users:
                gay_users.append(gay_to_add)
                bot.send_message(message.chat.id, f"Гей @{gay_to_add} добавлен в базу данных.")
            else:
                bot.send_message(message.chat.id, f"Гей @{gay_to_add} уже присутствует в базе данных.")
        else:
            bot.send_message(message.chat.id, "Укажите гея, которого нужно добавить.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

@bot.message_handler(commands=['checkremoved'])
def check_removed(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        if removed_gays:
            removed_list = "\n".join(removed_gays)
            bot.send_message(message.chat.id, f"Список геев которых нужно (наверно) удалить:\n{removed_list}")
        else:
            bot.send_message(message.chat.id, "Список геев которых нужно удалить пуст.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")
@bot.message_handler(commands=['removepredlozka'])
def remove_predlozka(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        predlozka.clear()
        bot.send_message(message.chat.id, "База данных предложенных геев очищена.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

@bot.message_handler(commands=['removeremoved'])
def remove_removed(message):
    if message.from_user.username in ["NE_RESHETO", "TYATYAPKA_FUN"]:
        removed_gays.clear()
        bot.send_message(message.chat.id, "База данных удаленных геев очищена.")
    else:
        bot.send_message(message.chat.id, "У вас нет доступа к этой команде.")

# Run the bot
bot.polling()