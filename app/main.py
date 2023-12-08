from telebot import TeleBot

from lib.credentials import get_credentials

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