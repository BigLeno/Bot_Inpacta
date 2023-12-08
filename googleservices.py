# Instalar antes de usar
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib.credentials import get_google_credentials

from logging import basicConfig, warning, info, INFO

# Definindo o nível do log
basicConfig(level=INFO)

# Mapeia índices para dias da semana
index_to_day = {1: 'Segunda', 2: 'Terça', 3: 'Quarta', 4: 'Quinta', 5: 'Sexta'}

# Variáveis utilizadas
client_directory, token_directory, scopes, sample_spreadsheet_id, sample_range_name = get_google_credentials()

def get_data_from_sheets():
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
      return

    info("Planilha acessada com sucesso!")
    info("Filtrando os dados...")

    for row in result:
      if all(item not in row for item in ['M12','N34','DIAS DA SEMANA']) and row:
          for i, item in enumerate(row):
            if item == 'X':
                day = index_to_day.get(i, 'Índice inválido')
                info(f"Não tem bolsista no horário da {day} às {row[0]}")
          
              

    info("Dados filtrados com sucesso!")

  except HttpError as err:
    warning(f"Foi encontrado um erro de conexão http {err}")


if __name__ == "__main__":
  get_data_from_sheets()