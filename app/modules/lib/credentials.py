from logging import info, warning
from os import getenv
from typing import Tuple

class Credentials:
    def __init__(self) -> None:
        """Função para inicializar as credenciais."""
        self.token = getenv('TOKEN')
        self.name_bot = getenv('NAME_BOT')
        self.admin = getenv('ADMIN')
        self.absolutepath = getenv('ABSOLUTE_PATH')
        self.cachedirectory = getenv('CACHE_DIRECTORY')
        self.user1 = getenv('USER_ID_1')
        self.user2 = getenv('USER_ID_2')
        self.user3 = getenv('USER_ID_3')
        self.user4 = getenv('USER_ID_4')
        self.user5 = getenv('USER_ID_5')
        self.user6 = getenv('USER_ID_6')
        self.username1 = getenv('USER_NAME_1')
        self.username2 = getenv('USER_NAME_2')
        self.username3 = getenv('USER_NAME_3')
        self.username4 = getenv('USER_NAME_4')
        self.username5 = getenv('USER_NAME_5')
        self.username6 = getenv('USER_NAME_6')
        self.client_directory = getenv('CLIENT_DIRECTORY')
        self.token_directory = getenv('TOKEN_DIRECTORY')
        self.scopes = getenv('SCOPES')
        self.sample_spreadsheet_id = getenv('SAMPLE_SPREADSHEET_ID')
        self.sample_range_name = getenv('SAMPLE_RANGE_NAME')

    def get_credentials(self) -> Tuple[str, str, str, str, str] or bool:
        """
            Função para pegar as credenciais do .env
        """
        if not all([self.token, self.name_bot, self.admin, self.absolutepath, self.cachedirectory]):
            warning("Uma ou mais variáveis de ambiente do telegram estão faltando.")
            return False
        else:
            info("Variáveis de ambiente do telegram carregadas com sucesso.")

        return self.token, self.name_bot, self.admin, self.absolutepath, self.cachedirectory

    def get_users_id(self) -> Tuple[str, str, str, str, str, str] or bool:
        """
            Função para pegar as credenciais do .env
        """
        if not all([self.user1, self.user2, self.user3, self.user4, self.user5, self.user6]):
            warning("Uma ou mais variáveis de ambiente de id dos usuários estão faltando.")
            return False
        else:
            info("Variáveis de ambiente de id dos usuários carregadas com sucesso.")

        return self.user1, self.user2, self.user3, self.user4, self.user5, self.user6

    def get_users_names(self) -> Tuple[str, str, str, str, str, str] or bool:
        """
            Função para pegar as credenciais do .env
        """
        if not all([self.username1, self.username2, self.username3, self.username4, self.username5, self.username6]):
            warning("Uma ou mais variáveis de ambiente de nome dos usuários estão faltando.")
            return False
        else:
            info("Variáveis de ambiente de nome dos usuários carregadas com sucesso.")

        return self.username1, self.username2, self.username3, self.username4, self.username5, self.username6

    def get_google_credentials(self) -> Tuple[str, str, str, str, str] or bool:
        """
            Função para pegar o diretório do client_secret
        """
        if not all([self.client_directory, self.token_directory, self.scopes, self.sample_spreadsheet_id, self.sample_range_name]):
            warning("Uma ou mais variáveis de ambiente do google estão faltando.")
            return False
        else:
            info("Variáveis de ambiente do google carregadas com sucesso.")

        return self.client_directory, self.token_directory, self.scopes, self.sample_spreadsheet_id, self.sample_range_name
