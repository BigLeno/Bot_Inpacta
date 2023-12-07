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
        warning("Uma ou mais variáveis de ambiente estão faltando.")
        return False
    else:
        info("Variáveis de ambiente carregadas com sucesso.")

    return token, name_bot, admin
