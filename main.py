import telebot
from extensions import APIException, CurrencyConverter
from config import TOKEN

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_instructions(message):
    text = "Введите сообщение в формате:\n<имя валюты, цену которой вы хотите узнать> " \
           "<имя валюты, в которой вы хотите узнать цену первой валюты> " \
           "<количество первой валюты>\n" \
           "Например: USD RUB 100\n\n" \
           "Доступные валюты: /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["values"])
def send_currencies(message):
    text = "Доступные валюты:\nUSD - доллар США\nEUR - евро\nRUB - российский рубль"
    bot.send_message(message.chat.id, text)


@bot.message_handler(content_types=["text"])
def get_price(message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException("Неверный формат ввода.")

        base, quote, amount = values
        total_price = CurrencyConverter.get_price(base.upper(), quote.upper(), float(amount))
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка: {e}")
        return

    text = f"{amount} {base.upper()} = {total_price} {quote.upper()}"
    bot.send_message(message.chat.id, text)


if __name__ == "__main__":
    bot.polling(none_stop=True)

