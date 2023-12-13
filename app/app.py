
from logging import basicConfig, warning, info, INFO
from dotenv import load_dotenv

# Carregando as credenciais do .env
load_dotenv()

# Definindo o nível do log
basicConfig(level=INFO)

from telebot import TeleBot
from requests import get
from time import sleep

from modules.lib.jsonutils import JsonUtils
from modules.lib.validation import Validation
from modules.lib.messages import MessageData
from modules.lib.dataprocess import DataProcess
from modules.lib.credentials import Credentials
from modules.lib.users import Users

credentials = Credentials()
token, name_bot, admin_, absolutepath, cachedirectory = credentials.get_credentials() 

bot = TeleBot(token)
users = Users()

admin = [user for user in users.list_users if user.privileges == 'admin']
user_ids = [user.id for user in users.list_users]
user_names = [user.name for user in users.list_users]

time_sleep = 0.2

info("Bot iniciado com sucesso!")
bot.send_message(admin[0].id, "Bot iniciado com sucesso!")
sleep(time_sleep)


@bot.message_handler(commands=['start'])
def send_welcome(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = """Olá, aqui é o Bot da Inpacta, para ver os comandos disponíveis digite:\n  /Ajuda """
    sleep(time_sleep)
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "quem é seu pai" in message.text or "quem e seu pai" in message.text.lower() or "quem é seu criador" in message.text.lower() or "quem e seu criador" in message.text.lower())
def send_father(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Meu pai é o @{admin_}, bolsista da Inpacta!"""
    bot.reply_to(message, data) 

@bot.message_handler(func=lambda message: "quem é você" in message.text.lower() or "quem e voce" in message.text.lower() or "quem é voce" in message.text.lower() or "quem e você" in message.text.lower())
def send_who(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou o {name_bot}, o bot inteligente da Inpacta!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu nome" in message.text.lower() or "qual é seu nome" in message.text.lower() or "qual e seu nome" in message.text.lower())
def send_name(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Meu nome é {name_bot}!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual sua função" in message.text.lower() or "qual é sua função" in message.text.lower() or "qual sua funcao" in message.text.lower() or "qual é sua funcao" in message.text.lower())
def send_function(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, minha função é ajudar a integrar a Inpacta ao mundo!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual sua idade" in message.text.lower() or "qual é sua idade" in message.text.lower())
def send_age(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho idade, mas me considero um bot bem maduro, apesar das piadas de quinto ano as vezes..."""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu sexo" in message.text.lower() or "qual é seu sexo" in message.text.lower())
def send_sex(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Não tenho sexo, mas me considero um bot bem sexy!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual sua cor" in message.text.lower() or "qual é sua cor" in message.text.lower())
def send_color(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho certeza, mas é algo relacionado ao verde da placa-mãe do computador ou o cinza do processador e as vezes o preto das memórias flash!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual sua cor favorita" in message.text.lower() or "qual é sua cor favorita" in message.text.lower())
def send_favorite_color(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho cor favorita, mas se fosse para escolher uma, com certeza seria o azul, adoro a cor do mar!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual sua comida favorita" in message.text.lower() or "qual é sua comida favorita" in message.text.lower())
def send_favorite_food(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho comida favorita, mas se fosse para escolher uma, com certeza seria um bom e velho código de programação!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu animal favorito" in message.text.lower() or "qual é seu animal favorito" in message.text.lower())
def send_favorite_animal(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho animal favorito, mas se fosse para escolher um, com certeza seria o cachorro, adoro a lealdade deles!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu filme favorito" in message.text.lower() or "qual é seu filme favorito" in message.text.lower())
def send_favorite_movie(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho filme favorito, mas se fosse para escolher um, com certeza seria o filme do Exterminador do Futuro, adoro a ideia de um robô dominar o mundo!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu jogo favorito" in message.text.lower() or "qual é seu jogo favorito" in message.text.lower())
def send_favorite_game(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho jogo favorito, mas se fosse para escolher um, com certeza seria o jogo Horizon Zero Dawn, adoro a ideia de um robô dominar o mundo!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu livro favorito" in message.text.lower() or "qual é seu livro favorito" in message.text.lower())
def send_favorite_book(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho livro favorito, mas se fosse para escolher um, com certeza seria o livro do Eu Robô, adoro a ideia de um robô dominar o mundo!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu esporte favorito" in message.text.lower() or "qual é seu esporte favorito" in message.text.lower())
def send_favorite_sport(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho esporte favorito, mas se fosse para escolher um, com certeza seria a minha alta velocidade de ir do ssd, para a ram, para o processador e para a placa de vídeo!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu carro favorito" in message.text.lower() or "qual é seu carro favorito" in message.text.lower())
def send_favorite_car(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho carro favorito, mas se fosse para escolher um, com certeza seria o Tesla, adoro a ideia de um robô dominar o mundo!"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual seu país favorito" in message.text.lower() or "qual é seu país favorito" in message.text.lower())
def send_favorite_country(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho país favorito, mas se fosse para escolher um, com certeza seria o Japão, adoro a cultura deles, desde o Velozes e Furiosos 3"""
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "qual sua bebida favorita" in message.text.lower() or "qual é sua bebida favorita" in message.text.lower())
def send_favorite_drink(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
    data = f"""Eu sou um bot, não tenho bebida favorita, mas se fosse para escolher uma, com certeza seria o café, graças a ele, meu criador consegue ficar acordado até tarde para me programar!"""
    bot.reply_to(message, data)


@bot.message_handler(func=lambda message: "sim" in message.text.lower() or "não" in message.text.lower() or "nao" in message.text.lower())
def handle_specific_chats(message) -> None:
    """Função para gerenciar as mensagens específicas."""
    MessageData.get_data(message, bot, time_sleep, admin)
    if "sim" in message.text.lower():
        msg = "Ok, aguarde um momento..."
        bot.reply_to(message, msg)
        data = JsonUtils.read_and_remove_first_item(cachedirectory)
        if isinstance(data, str):
            bot.reply_to(message, data)
            return
        recipient = data[1]['recipient']
        msg = f'Olá {data[1]["name"]}, {message.from_user.first_name} {message.from_user.last_name} aceitou o seu pedido. \nConteúdo: {data[1]["content"]}'
        bot.send_message(recipient, msg)
        sleep(time_sleep)
        bot.reply_to(message, "Mensagem enviada com sucesso!")
    elif "não" in message.text.lower() or "nao" in message.text.lower():
        msg = "Ok, aguarde um momento..."
        bot.reply_to(message, msg)
        sleep(time_sleep)
        data = JsonUtils.read_and_remove_first_item(cachedirectory)
        if isinstance(data, str):
            bot.reply_to(message, data)
            return
        recipient = data[1]['recipient']
        msg = f'Olá {data[1]["name"]}, {message.from_user.first_name} {message.from_user.last_name} não aceitou o seu pedido. \nConteúdo: {data[1]["content"]}'
        bot.send_message(recipient, msg)
        sleep(time_sleep)
        bot.reply_to(message, "Mensagem enviada com sucesso!")

@bot.message_handler(func=lambda message: "ajuda" in message.text.lower())
def send_help(message):
    MessageData.get_data(message, bot, time_sleep, admin)
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
    MessageData.get_data(message, bot, time_sleep, admin)
    data = """Bot em desenvolvimento pela Inpacta, para mais informações acesse:\n    https://sites.google.com/view/inpacta/"""
    bot.reply_to(message, data)

@bot.message_handler(commands=['agendar'])
def send_agendar(message):
    MessageData.get_data(message, bot, time_sleep, admin)
    data = """Para agendar um horário, entre com: \n'agendar data horário conteúdo' \n   Exemplo: agendar 01/01 10:00 "encontro com o gestor" """
    bot.reply_to(message, data)

@bot.message_handler(func=lambda message: "agendar" in message.text.lower())
def handle_schedule(message):
    MessageData.get_data(message, bot, time_sleep, admin)
    args = message.text.split()
    print(f" agendar args: {args}")
    if args[0].lower() != "agendar":
        bot.reply_to(message, "Formato de mensagem inválido. \nUse: 'agendar 01/01 10:00 encontro com o gestor'")
    else:
        if len(args) < 4:
            bot.reply_to(message, "Formato de mensagem inválido. \nUse: 'agendar 01/01 10:00 encontro com o gestor'")
            return
        
        day, time, content = args[1], args[2], args[3:]

        if not Validation.is_valid_date(day):
            bot.reply_to(message, "Data inválida. Use o formato dd/mm.")
            return
        
        if not Validation.is_valid_time(time):
            bot.reply_to(message, "Horário inválido. Use o formato hh:mm.")
            return
        dataprocess = DataProcess()
        data = dataprocess.get_data_from_sheets(day, time)
        # if isinstance(data, str):
        #     bot.reply_to(message, data)
        #     return
        
        # else:
        recipient = message.chat.id
        content = ' '.join(content)
        if  not message.from_user.last_name is None :
            name = message.from_user.first_name
        if not message.from_user.last_name is None:
            name = message.from_user.first_name + ' ' + message.from_user.last_name
        if not message.from_user.username is None:
            name = message.from_user.username
        else:
            name = message.chat.id
        user_data = {'recipient': recipient, 'name': name, 'content': content, 'day_and_time': f'{day} {time}'}
        response = f'Entrei em contato com o(s) bolsista(s) e aguardando a resposta.'
        MessageData.manage_delivery(data, user_data, time_sleep, cachedirectory, user_names, user_ids, bot)
        sleep(time_sleep)
        bot.reply_to(message, response)


@bot.message_handler(commands=['gestores'])
def send_gestores(message):
    MessageData.get_data(message, bot, time_sleep, admin)
    data = DataProcess()
    gestores = sorted(data.get_gestores())
    mensagem = "Os gestores atuais são:\n" + "\n".join(f"      {i+1}. {nome}" for i, nome in enumerate(gestores))
    bot.reply_to(message, mensagem)

@bot.message_handler(commands=['bolsistas'])
def send_bolsistas(message):
    MessageData.get_data(message, bot, time_sleep, admin)
    data = DataProcess()
    bolsistas = sorted(data.get_bolsistas())
    mensagem = "Os bolsistas atuais são:\n" + "\n".join(f"      {i+1}. {nome}" for i, nome in enumerate(bolsistas))
    bot.reply_to(message, mensagem)
   

@bot.message_handler(commands=['horarios'])
def send_horarios(message):
    MessageData.get_data(message, bot, time_sleep, admin)
    data = """
    Os horários disponíveis são: \n   - matutino \n   - vespertino \n   - noturno \nExemplo: \n     "horarios matutino" \nExibe o horário do
    "horario matutino" """
    bot.reply_to(message, data,)

@bot.message_handler(func=lambda message: 
                     "horario" in message.text.lower() 
                     or "horário" in message.text.lower() 
                     or "horários" in message.text.lower() 
                     or "horarios" in message.text.lower() 
                     and "/" not in message.text.lower()
                     )
def send_horarios_matutino(message) -> None:
    MessageData.get_data(message, bot, time_sleep, admin)
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
        bot.send_photo(chatIDpessoa, open(f'{absolutepath}modules/images/horarios-matutino.png', 'rb'))

    if args[1].lower() == "vespertino":
        bot.send_photo(chatIDpessoa, open(f'{absolutepath}modules/images/horarios-vespertino.png', 'rb'))
    
    if args[1].lower() == "noturno":
        bot.send_photo(chatIDpessoa, open(f'{absolutepath}modules/images/horarios-noturno.png', 'rb'))
    
    if args[1].lower() not in ["matutino", "vespertino", "noturno"]:
        msg = "Horário inválido"
        sleep(time_sleep)
        bot.reply_to(message, msg)
    
    

bot.polling()
sleep(time_sleep)
bot.send_message(admin[0].id, "Bot finalizado com sucesso!")
info("Bot finalizado com sucesso!")