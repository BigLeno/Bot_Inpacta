# Instalar antes de usar
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from lib.credentials import get_google_credentials


# Variáveis utilizadas
client_directory, token_directory, scopes, SAMPLE_SPREADSHEET_ID, SAMPLE_RANGE_NAME = get_google_credentials()

def main():
  """
    Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
  """

  creds = None
  if os.path.exists(token_directory):
    creds = Credentials.from_authorized_user_file(token_directory, [scopes])
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          client_directory, [scopes]
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(token_directory, "w") as token:
      token.write(creds.to_json())

  # try:
  #   service = build("sheets", "v4", credentials=creds)

  #   # Call the Sheets API
  #   sheet = service.spreadsheets()
  #   result = (
  #       sheet.values()
  #       .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
  #       .execute()
  #   )
  #   values = result.get("values", [])

  #   if not values:
  #     print("No data found.")
  #     return

  #   print("Name, Major:")
  #   for row in values:
  #     # Print columns A and E, which correspond to indices 0 and 4.
  #     print(f"{row[0]}, {row[4]}")
  # except HttpError as err:
  #   print(err)


if __name__ == "__main__":
  main()