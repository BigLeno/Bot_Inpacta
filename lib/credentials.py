from dotenv import load_dotenv
from os import getenv

from logging import basicConfig, warning, info, INFO
from typing import Tuple

def get_credentials() -> Tuple[str, str, str]:
    """
        Função para pegar as credenciais do .env
    """
    basicConfig(level=INFO)
    load_dotenv()
    token = getenv('TOKEN')
    name_bot = getenv('NAME_BOT')
    admin = getenv('ADMIN')

    if not token or not name_bot or not admin:
        warning("Uma ou mais variáveis de ambiente do telegram estão faltando.")
        return False
    else:
        info("Variáveis de ambiente do telegram carregadas com sucesso.")

    return token, name_bot, admin

def get_google_credentials() -> Tuple[str]:
    """
        Função para pegar o diretório do client_secret
    """
    basicConfig(level=INFO)
    load_dotenv()
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
