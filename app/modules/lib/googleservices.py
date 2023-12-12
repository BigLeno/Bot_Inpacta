# Instalar antes de usar
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Somente quando for rodar localmente
# from credentials import get_google_credentials

from modules.lib.credentials import get_google_credentials

from logging import warning, info

class GoogleSheets:

  def __init__(self, sample_range_name='', sample_spreadsheet_id='') -> None:
    """Função para inicializar a planilha do googleSheets.
    Args:
        sample_range_name (str, optional): Nome da planilha. Defaults to ''.
        sample_spreadsheet_id (str, optional): Id da planilha. Defaults to ''.
    """
    if not sample_range_name or not sample_spreadsheet_id:
      self.client_directory, self.token_directory, self.scopes, self.sample_spreadsheet_id, self.sample_range_name = get_google_credentials()
    if sample_range_name:
      self.sample_range_name = sample_range_name
    if sample_spreadsheet_id:
      self.sample_spreadsheet_id = sample_spreadsheet_id
    info("Inicializando planilha do googleSheets...")
    self.port = 0
    self.creds = None
    self.get_and_verify_acess()

  def get_and_verify_acess(self) -> None:
    """Função para pegar e verificar o acesso da planilha do googleSheets."""
    if os.path.exists(self.token_directory):
      self.creds = Credentials.from_authorized_user_file(self.token_directory, [self.scopes])
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(self.client_directory, [self.scopes])
        self.creds = flow.run_local_server(port=self.port)
      with open(self.token_directory, "w") as token:
        token.write(self.creds.to_json())

  def get_sheets(self):
    """Função para pegar os dados da planilha do googleSheets."""
    try:
      service = build("sheets", "v4", credentials=self.creds)
      sheet = service.spreadsheets()
      result = (sheet.values().get(spreadsheetId=self.sample_spreadsheet_id, range=self.sample_range_name).execute()).get("values", [])

      if not result:
        warning("Não foi encontrando nenhum dado na planilha do googleSheets.")
        return False

      info("Planilha acessada com sucesso!")
      return result

    except HttpError as err:
        warning(f"Foi encontrado um erro de conexão http {err}")
        return False




