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

# Mapeia dias da semana para índices
day_to_index = {'Segunda': 1, 'Terça': 2, 'Quarta': 3, 'Quinta': 4, 'Sexta': 5}

# Lista de horários permitidos
allowed_times = ['M12', 'M34', 'M56', 'T12', 'T34', 'T56', 'N12', 'N34']

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

def get_data_from_sheets(day, time):

    result = get_sheets()

    if not result:
      return False

    day_index = day_to_index.get((day.lower()).capitalize(), -1)
    formated_time = (time.lower()).capitalize()

    for row in result:
      if all(item not in row for item in ['M12','N34','DIAS DA SEMANA']) and row:
          if (row[0] == formated_time and 
            0 < day_index < len(row) and 
            formated_time in allowed_times and 
            row[day_index] != 'X'):

            bolsistas = [bolsista.strip() for bolsista in row[day_index].split('/')]

            if len(bolsistas) == 1:
                info("Bolsista encontrado!")
                return f"Bolsista: {bolsistas[0]}"
            elif len(bolsistas) == 2:
                info("Dois bolsistas encontrados!")
                return f"Bolsistas: {bolsistas[0]} e {bolsistas[1]}"
            elif len(bolsistas) == 3:
                info("Três bolsistas encontrados!")
                return f"Bolsistas: {bolsistas[0]}, {bolsistas[1]} e {bolsistas[2]}"
            
          elif (row[0] == formated_time and 
              row[day_index] == 'X' and 
              formated_time in allowed_times and 
              0 < day_index < len(row)):
            
            info("Horário vazio")
            return "Não tem bolsista neste horário."
          
          elif formated_time not in allowed_times and 0 < day_index < len(row):
            warning("Horário inválido.")
            return False
          
          elif not (0 < day_index < len(row)):
            warning("Dia inválido.")
            return False


# if __name__ == "__main__":
#   day = input("Digite o dia: ")
#   time = input("Digite a hora: ")
#   print(get_data_from_sheets(day, time))