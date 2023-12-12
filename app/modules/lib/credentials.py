from logging import info, warning
from os import getenv
from typing import Tuple

from dotenv import load_dotenv


def get_credentials() -> Tuple[str, str, str, str, str]:
    """
        Função para pegar as credenciais do .env
    """
    token = getenv('TOKEN')
    name_bot = getenv('NAME_BOT')
    admin = getenv('ADMIN')
    absolutepath = getenv('ABSOLUTE_PATH')
    cachedirectory = getenv('CACHE_DIRECTORY')

    if not token or not name_bot or not admin or not absolutepath or not cachedirectory:
        warning("Uma ou mais variáveis de ambiente do telegram estão faltando.")
        return False
    else:
        info("Variáveis de ambiente do telegram carregadas com sucesso.")

    return token, name_bot, admin, absolutepath, cachedirectory

def get_users_id() -> Tuple[str, str, str, str, str, str]:
    """
        Função para pegar as credenciais do .env
    """
    user1 = getenv('USER_ID_1')
    user2 = getenv('USER_ID_2')
    user3 = getenv('USER_ID_3')
    user4 = getenv('USER_ID_4')
    user5 = getenv('USER_ID_5')
    user6 = getenv('USER_ID_6')

    if not user1 or not user2 or not user3 or not user4 or not user5 or not user6:
        warning("Uma ou mais variáveis de ambiente de id dos usuários estão faltando.")
        return False
    else:
        info("Variáveis de ambiente de id dos usuários carregadas com sucesso.")

    return user1, user2, user3, user4, user5, user6

def get_users_names() -> Tuple[str, str, str, str, str, str]:
    """
        Função para pegar as credenciais do .env
    """
    
    username1 = getenv('USER_NAME_1')
    username2 = getenv('USER_NAME_2')
    username3 = getenv('USER_NAME_3')
    username4 = getenv('USER_NAME_4')
    username5 = getenv('USER_NAME_5')
    username6 = getenv('USER_NAME_6')

    if not username1 or not username2 or not username3 or not username4 or not username5 or not username6:
        warning("Uma ou mais variáveis de ambiente de nome dos usuários estão faltando.")
        return False
    else:
        info("Variáveis de ambiente de nome dos usuários carregadas com sucesso.")

    return username1, username2, username3, username4, username5, username6

def get_google_credentials() -> Tuple[str]:
    """
        Função para pegar o diretório do client_secret
    """
    
    client_directory = getenv('CLIENT_DIRECTORY')
    token_directory = getenv('TOKEN_DIRECTORY')
    scopes = getenv('SCOPES')
    sample_spreadsheet_id = getenv('SAMPLE_SPREADSHEET_ID')
    sample_range_name = getenv('SAMPLE_RANGE_NAME')

    if not client_directory or not token_directory or not scopes or not sample_spreadsheet_id or not sample_range_name:
        warning("Uma ou mais variáveis de ambiente do google estão faltando.")
        return False
    else:
        info("Variáveis de ambiente do google carregadas com sucesso.")

    return client_directory, token_directory, scopes, sample_spreadsheet_id, sample_range_name
