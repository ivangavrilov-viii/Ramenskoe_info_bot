import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


# Имя файла с закрытым ключом
CREDENTIALS_FILE = 'ramenskoe-bot-table-fcb7a2637170.json'

# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1Byf0RirVeh2v0qLuf6XUiL588dNwuGKLKvIRUNthgeg'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)


# Функция добавляет значения info
def insert_values(info):
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        valueInputOption="USER_ENTERED",
        range="Users!A1",
        body={
            # "values": [
            #     ["User ID", "Номер телефона", "ИНН", "Имя пользователя", "Фамилия пользователя",
            #      "Username", "Начало сеанса", "Конец сеанса", "Путь по боту"]
            # ]
            "values": [info]
        }
    ).execute()

