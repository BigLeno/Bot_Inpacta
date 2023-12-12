
from logging import basicConfig, warning, info, INFO
from telebot import TeleBot
from requests import get
from uuid import uuid4
from time import strptime, sleep

from modules.lib.credentials import get_credentials
from modules.lib.dataprocess import get_data_from_sheets
from modules.lib.users import Users
from modules.lib.jsonutils import write_json, read_and_remove_first_item


# Definindo o nível do log
basicConfig(level=INFO)

token, name_bot, admin, absolutepath, cachedirectory = get_credentials() 

bot = TeleBot(token)
users = Users()

admin = [user for user in users.list_users if user.privileges == 'admin']
user_ids = [user.id for user in users.list_users]
user_names = [user.name for user in users.list_users]

time_sleep = 0.2

info("Bot iniciado com sucesso!")
get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={"Bot iniciado com sucesso!"}')
sleep(time_sleep)


def is_valid_date(date_str) -> bool:
    """Verifica se a data está no formato dd/mm."""

    if date_str in ['hoje', 'amanhã', 'amanha']:
        return True

    try:
        strptime(date_str, '%d/%m')
        return True
    except ValueError:
        return False

def is_valid_time(time_str) -> bool:
    """Verifica se o horário está no formato hh:mm."""
    formats = ['%H:%M', '%Hh', '%Hh%M', '%HH', '%HH%M']
    for fmt in formats:
        try:
            strptime(time_str, fmt)
            return True
        except ValueError:
            continue
    return False
    
def get_data(message):
    chatid = message.chat.id
    usuario = message.from_user.username
    nome = message.from_user.first_name
    sobrenome = message.from_user.last_name
    text = message.text
    info("Dados do usuário carregados.")
    mensagem = f"""ChatID: {chatid}\nUsuário: {usuario}\nNome e sobrenome : {nome} {sobrenome}\nMensagem: {text}"""
    sleep(time_sleep)
    get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={mensagem}')

@bot.message_handler(commands=['start'])
def send_welcome(message) -> None:
    get_data(message)
    data = """Olá, aqui é o Bot da Inpacta, para ver os comandos disponíveis digite:\n  /Ajuda """
    sleep(time_sleep)
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "sim" in message.text.lower() or "não" in message.text.lower() or "nao" in message.text.lower())
def handle_specific_chats(message) -> None:
    """Função para gerenciar as mensagens específicas."""
    get_data(message)
    if "sim" in message.text.lower():
        msg = "Ok, aguarde um momento..."
        bot.reply_to(message, msg)
        data = read_and_remove_first_item(cachedirectory)
        if isinstance(data, str):
            bot.reply_to(message, data)
            return
        recipient = data[1]['recipient']
        msg = f'Olá {data[1]["name"]}, {message.from_user.first_name} {message.from_user.last_name} aceitou o seu pedido. \nConteúdo: {data[1]["content"]}'
        get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={recipient}&text={msg}')
        sleep(time_sleep)
        bot.reply_to(message, "Mensagem enviada com sucesso!")
    elif "não" in message.text.lower() or "nao" in message.text.lower():
        msg = "Ok, aguarde um momento..."
        bot.reply_to(message, msg)
        sleep(time_sleep)
        data = read_and_remove_first_item(cachedirectory)
        if isinstance(data, str):
            bot.reply_to(message, data)
            return
        recipient = data[1]['recipient']
        msg = f'Olá {data[1]["name"]}, {message.from_user.first_name} {message.from_user.last_name} não aceitou o seu pedido. \nConteúdo: {data[1]["content"]}'
        get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={recipient}&text={msg}')
        sleep(time_sleep)
        bot.reply_to(message, "Mensagem enviada com sucesso!")

@bot.message_handler(func=lambda message: "ajuda" in message.text.lower())
def send_help(message):
    get_data(message)
    data = """
    Comandos disponíveis:
    /horarios - Exibe os horários
    /agendar - Agenda um horário
    /bolsistas - Exibe os bolsistas
    /gestores - Exibe os gestores
    /sobre - Exibe informações sobre o bot
    /ajuda - Exibe os comandos disponíveis
    """
    bot.reply_to(message, data)

@bot.message_handler(commands=['sobre'])
def send_sobre(message):
    get_data(message)
    data = """Bot em desenvolvimento pela Inpacta, para mais informações acesse:\n    https://sites.google.com/view/inpacta/"""
    bot.reply_to(message, data)

@bot.message_handler(commands=['agendar'])
def send_agendar(message):
    get_data(message)
    data = """Para agendar um horário, entre com: \n'agendar data horário conteúdo' \n   Exemplo: agendar 01/01 10:00 "encontro com o gestor" """
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "agendar" in message.text.lower())
def handle_schedule(message):
    get_data(message)
    args = message.text.split()
    print(f" agendar args: {args}")
    if args[0].lower() != "agendar":
        bot.reply_to(message, "Formato de mensagem inválido. \nUse: 'agendar 01/01 10:00 encontro com o gestor'")
    else:
        if len(args) < 4:
            bot.reply_to(message, "Formato de mensagem inválido. \nUse: 'agendar 01/01 10:00 encontro com o gestor'")
            return
        
        day, time, content = args[1], args[2], args[3:]

        if not is_valid_date(day):
            bot.reply_to(message, "Data inválida. Use o formato dd/mm.")
            return
        
        if not is_valid_time(time):
            bot.reply_to(message, "Horário inválido. Use o formato hh:mm.")
            return
        
        data = get_data_from_sheets(day, time)
        if isinstance(data, str):
            bot.reply_to(message, data)
            return
        
        else:
            recipient = message.chat.id
            content = ' '.join(content)
            name = message.from_user.first_name + ' ' + message.from_user.last_name
            user_data = {'recipient': recipient, 'name': name, 'content': content, 'day_and_time': f'{day} {time}'}
            response = f'Entrei em contato com o(s) bolsista(s) e aguardando a resposta.'
            manage_delivery(data, user_data)
            sleep(time_sleep)
            bot.reply_to(message, response)


def manage_delivery( data:tuple, user_data:dict):
    """Função para gerenciar a entrega da mensagem."""
    try:
        identificador = str(uuid4())
        write_json(user_data, identificador, cachedirectory)
    except Exception as err:
        warning(f"Não foi possível escrever no arquivo json. {err}")
        return
    
    for name in user_names:
        if name in data:
            recipient = user_ids[user_names.index(name)]
            msg = f'Olá {name}, {user_data["name"]} quer agendar um horário com você no dia {user_data["day_and_time"]}. \nConteúdo: {user_data["content"]}'
            sleep(time_sleep)
            get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={recipient}&text={msg}')


@bot.message_handler(commands=['gestores'])
def send_gestores(message):
    get_data(message)
    data = """
    Em desenvolvimento..."""
    bot.reply_to(message, data)

@bot.message_handler(commands=['bolsistas'])
def send_bolsistas(message):
    get_data(message)
    data = """
    Em desenvolvimento..."""
    bot.reply_to(message, data)

@bot.message_handler(commands=['horarios'])
def send_horarios(message):
    get_data(message)
    data = """
    Os horários disponíveis são: \n   > matutino \n   > vespertino \n   > noturno \nExemplo: \n     "horarios matutino" \nExibe o horário do
    "horario matutino" """
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: 
                     "horario" in message.text.lower() 
                     or "horário" in message.text.lower() 
                     or "horários" in message.text.lower() 
                     or "horarios" in message.text.lower() 
                     and "/" not in message.text.lower()
                     )
def send_horarios_matutino(message) -> None:
    get_data(message)
    chatIDpessoa=message.chat.id
    bot.reply_to(message, "Aguarde um momento...")
    args = message.text.split()
    print(f" horarios args: {args}")

    if len(args) < 2:
        msg = "Formato de mensagem inválido! \nPor favor, use: \n   'horarios matutino'"
        sleep(time_sleep)
        bot.reply_to(message, msg)
        return

    if args[1].lower() == "matutino":
        msg = "Horário do turno Matutino"
        img = open(f"{absolutepath}modules/images/horarios-matutino.png", 'rb')
        sleep(time_sleep)
        get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
    
    if args[1].lower() == "vespertino":
        msg = "Horário do turno Vespertino"
        img = open(f"{absolutepath}modules/images/horarios-vespertino.png", 'rb')
        sleep(time_sleep)
        get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
    
    if args[1].lower() == "noturno":
        msg = "Horário do turno Noturno"
        img = open(f"{absolutepath}modules/images/horarios-noturno.png", 'rb')
        sleep(time_sleep)
        get(f'https://api.telegram.org/bot{token}/sendPhoto?chat_id={chatIDpessoa}&caption={msg}', files={'photo': img})
    
    if args[1].lower() not in ["matutino", "vespertino", "noturno"]:
        msg = "Horário inválido"
        sleep(time_sleep)
        bot.reply_to(message, msg)
    
    

bot.polling()
sleep(time_sleep)
get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={"Bot finalizado com sucesso!"}')
info("Bot finalizado com sucesso!")