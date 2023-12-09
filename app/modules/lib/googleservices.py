# Instalar antes de usar
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Somente quando for rodar localmente
from credentials import get_google_credentials

# from modules.lib.credentials import get_google_credentials

from logging import basicConfig, warning, info, INFO

# Definindo o nível do log
basicConfig(level=INFO)



# Variáveis de ambiente utilizadas
client_directory, token_directory, scopes, sample_spreadsheet_id, sample_range_name = get_google_credentials()

def get_sheets():
  creds = None
  if os.path.exists(token_directory):
    creds = Credentials.from_authorized_user_file(token_directory, [scopes])
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(client_directory, [scopes])
      creds = flow.run_local_server(port=0)
    with open(token_directory, "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)
    sheet = service.spreadsheets()
    result = (sheet.values().get(spreadsheetId=sample_spreadsheet_id, range=sample_range_name).execute()).get("values", [])

    if not result:
      warning("Não foi encontrando nenhum dado na planilha do googleSheets.")
      return False

    info("Planilha acessada com sucesso!")
    return result

  except HttpError as err:
      warning(f"Foi encontrado um erro de conexão http {err}")
      return False




