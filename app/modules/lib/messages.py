
from logging import info, warning
from requests import get
from uuid import uuid4
from time import sleep

from modules.lib.jsonutils import write_json

def get_data(message, token:str, time_sleep:int or float, admin:list)-> None:
    """Função para carregar os dados do usuário."""
    chatid = message.chat.id
    usuario = message.from_user.username
    nome = message.from_user.first_name
    sobrenome = message.from_user.last_name
    text = message.text
    info("Dados do usuário carregados.")
    mensagem = f"""ChatID: {chatid}\nUsuário: {usuario}\nNome e sobrenome : {nome} {sobrenome}\nMensagem: {text}"""
    sleep(time_sleep)
    get(f'https://api.telegram.org/bot{token}/sendmessage?chat_id={admin[0].id}&text={mensagem}')

def manage_delivery(data:tuple, user_data:dict, time_sleep:float or int, cachedirectory:str, user_names:list, user_ids:list, token:str) -> None:
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