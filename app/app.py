from telebot import TeleBot

from modules.lib.credentials import get_credentials
from modules.lib.googleservices import get_data_from_sheets

token, name_bot, admin = get_credentials() 

bot = TeleBot(token)

def verify(mensagem):
    if mensagem.text == "start":
        return True
    else:
        return False

@bot.message_handler(func=verify)
def responder(mensagem):
    print(mensagem)
    bot.reply_to(mensagem, "Olá, aqui é o Bot da Inpacta")
    print()

bot.polling()