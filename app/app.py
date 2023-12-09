
from logging import basicConfig, warning, info, INFO
from telebot import TeleBot
from requests import get

from modules.lib.credentials import get_credentials
from modules.lib.dataprocess import get_data_from_sheets
from modules.lib.users import Users


# Definindo o nível do log
basicConfig(level=INFO)

token, name_bot, admin = get_credentials() 

bot = TeleBot(token)

users = Users()
admin = [user for user in users.list_users if user.privileges == 'admin']

info("Bot iniciado com sucesso!")
get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={"Bot iniciado com sucesso!"}')
    
def get_data(message):
    chatid = message.chat.id
    usuario = message.from_user.username
    nome = message.from_user.first_name
    sobrenome = message.from_user.last_name
    text = message.text
    mensagem = f"""ChatID: {chatid}\nUsuário: {usuario}\nNome e sobrenome : {nome} {sobrenome}\nMensagem: {text}"""
    get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={mensagem}')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    get_data(message)
    data = """Olá, aqui é o Bot da Inpacta, para ver os comandos disponíveis digite:\n  /Ajuda """
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "ajuda" in message.text.lower())
def send_help(message):
    get_data(message)
    data = """
    Comandos disponíveis:
    /horarios - Exibe os horários
    /agendar - Agenda um horário
    /bolsistas - Exibe os bolsistas
    /coordenadores - Exibe os coordenadores
    /sobre - Exibe informações sobre o bot
    /ajuda - Exibe os comandos disponíveis
    """
    bot.reply_to(message, data)

@bot.message_handler(commands=['sobre'])
def send_sobre(message):
    get_data(message)
    data = """
    Bot desenvolvido pela Inpacta, para mais informações acesse: https://sites.google.com/view/inpacta/"""
    bot.reply_to(message, data)

@bot.message_handler(commands=['agendar'])
def send_agendar(message):
    get_data(message)
    data = """
    Em desenvolvimento..."""
    bot.reply_to(message, data)

@bot.message_handler(commands=['coordenadores'])
def send_coordenadores(message):
    get_data(message)
    data = """
    Em desenvolvimento..."""
    bot.reply_to(message, data)

@bot.message_handler(commands=['bolsistas'])
def send_horarios(message):
    get_data(message)
    data = """
    Em desenvolvimento..."""
    bot.reply_to(message, data)

@bot.message_handler(commands=['horarios'])
def send_horarios(message):
    get_data(message)
    data = """
    Para ver os horários disponíveis digite:
    "horario matutino" (Matutino, Vespertino ou Noturno)"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "horario" in message.text.lower() or "horário" in message.text.lower())
def send_horarios_matutino(message):
    get_data(message)
    chatIDpessoa=message.chat.id
    bot.reply_to(message, "Aguarde um momento...")
    print(chatIDpessoa)

    if "matutino" in message.text.lower():
        msg = "Horário do turno Matutino"
        img = open(f"app/modules/images/horarios-matutino.png", 'rb')
        get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
    
    if "vespertino" in message.text.lower():
        msg = "Horário do turno Vespertino"
        img = open(f"app/modules/images/horarios-vespertino.png", 'rb')
        get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
    
    if "noturno" in message.text.lower():
        msg = "Horário do turno Noturno"
        img = open(f"app/modules/images/horarios-noturno.png", 'rb')
        get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
    
    if "matutino" not in message.text.lower() and "vespertino" not in message.text.lower() and "noturno" not in message.text.lower():
        msg = "Horário inválido"
        bot.reply_to(message, msg)
    
    

bot.polling()
get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={"Bot finalizado com sucesso!"}')
info("Bot finalizado com sucesso!")