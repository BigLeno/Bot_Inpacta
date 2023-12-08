from telebot import TeleBot

from modules.lib.credentials import get_credentials
from modules.lib.googleservices import get_data_from_sheets

from logging import basicConfig, warning, info, INFO

# Definindo o nível do log
basicConfig(level=INFO)

token, name_bot, admin = get_credentials() 

bot = TeleBot(token)

info("Bot iniciado com sucesso!")

def ajuda(message):
    if message.text == "ajuda":
        return True


@bot.message_handler(commands=['start'])
def send_welcome(message):
    data = """
    Olá, aqui é o Bot da Inpacta digite "ajuda" para ver os comandos disponíveis"""
    bot.reply_to(message, data)

@bot.message_handler(func=ajuda)
def send_help(message):
    data = """
    Comandos disponíveis:
    /horarios - Exibe os horários
    /agendar - Agenda um horário
    /bolsistas - Exibe os bolsistas"""
    bot.reply_to(message, data)

@bot.message_handler(commands=['horarios'])
def send_horarios(message):
    data = """
    Horários disponíveis:
    Segunda: 12h, 14h, 16h
    Terça: 12h, 14h, 16h
    Quarta: 12h, 14h, 16h
    Quinta: 12h, 14h, 16h
    Sexta: 12h, 14h, 16h"""
    bot.reply_to(message, data)

bot.polling()
info("Bot finalizado com sucesso!")