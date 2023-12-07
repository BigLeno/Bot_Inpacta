from telebot import TeleBot

from dotenv import load_dotenv
from os import getenv


load_dotenv()
token = getenv('TOKEN')
nameBot = getenv('NAME_BOT')
userAdmin = getenv('ADMIN')

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