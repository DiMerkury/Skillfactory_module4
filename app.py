import telebot

from extensions import APIException, CurrencyConversion

from conf import keys
from mytoken import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
    text = 'Для использования бота введите комманду в следующем формате:\n <начальная валюта> <валюта в которую хотите перевести> <колличество валюты которую хотите перевести>\n \
Для просмотра списка валют введите /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        if len(values) != 3:
            raise APIException('Не верный список параметров.')
        
        quote, base, amount = values

        total_base = CurrencyConversion.get_price(quote, base, amount)

    except APIException as e:
        text = f'Ошибка ввода параметров. {e}'
    except Exception as system_e:
        text = f'Системная ошибка. {system_e}'
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
    
    bot.reply_to(message, text)
    #bot.send_message(message.chat.id, text)

bot.polling()
