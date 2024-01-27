import telebot

from Properties import TOKEN, currency
from BotClasses import ConvertionException, CryptoConverter

from Messages import list_of_start_messages
from random import choice

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    bot.reply_to(message, choice(list_of_start_messages), parse_mode="Markdown")


@bot.message_handler(commands=["help"])
def bot_help(message: telebot.types.Message):
    text = ("Добро пожаловать в CMoneyBot - твоего персонального ассистента по конвертации валют!\n"
            "Чтобы использовать бота, просто отправьте мне сообщение с необходимой командой или текстом:\n\n"
            "Для ковертации введи текст в формате: *<из валюты> <в валюту> <сумма>*\n\n"
            "Пример ввода: Доллар Рубль 1\n"
            "Пример вывода: 1 Доллар в Рубль - 100\n\n"
            "Для вывода стартового сообщения введи */start*\n"
            "Для просмотра всех доступных валют введи */values*\n")
    bot.reply_to(message, text, parse_mode="Markdown")


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = ["*Валюты доступные для перевода:*"]
    text += [f"{" " * 10}{i.capitalize()}" for i in currency.keys()]
    bot.reply_to(message, "\n".join(text), parse_mode="Markdown")


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        input_price_string = [i.lower() for i in message.text.split()]

        if len(input_price_string) != 3:
            raise ConvertionException("Слишком много параметров!")

        price_from, price_to, quantity = input_price_string

        total = CryptoConverter.convert(price_from, price_to, quantity)
    except ConvertionException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"{quantity} {price_from.capitalize()} в {price_to.capitalize()} - *{total * int(quantity)}*"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")


bot.polling()
