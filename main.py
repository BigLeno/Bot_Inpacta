import telebot

nameBot = '@Inpacta_bot'

user = ['Rutileno_Gabriel']

token = '6659921589:AAG0GDyZFJt1thxg1r6WkhqeNPvlk0wh19Q'

bot = telebot.TeleBot(token)

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