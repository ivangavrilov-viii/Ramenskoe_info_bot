import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials


# Имя файла с закрытым ключом, вы должны подставить свое
CREDENTIALS_FILE = 'ramenskoe-bot-table-fcb7a2637170.json'

# Читаем ключи из файла
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE,
                                                               ['https://www.googleapis.com/auth/spreadsheets',
                                                                'https://www.googleapis.com/auth/drive'])

# Авторизуемся в системе
httpAuth = credentials.authorize(httplib2.Http())

# Выбираем работу с таблицами и 4 версию API
service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

# Меняем название таблицы 'NAME_OF_SHEET' на своё, кол-во строчек и столбцов, Название страницы
spreadsheet = service.spreadsheets().create(body={
    'properties': {'title': 'Ramenskoe_info_telegram_bot', 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Пользователи',
                               'gridProperties': {'rowCount': 1000000, 'columnCount': 10}}}]
}).execute()


# Записываем адрес таблицы
spreadsheetId = spreadsheet['spreadsheetId']

# Выводим адрес таблицы для дальнейшего использования
print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)

# Выбираем работу с Google Drive и 3 версию API
driveService = apiclient.discovery.build('drive', 'v3', http=httpAuth)
access = driveService.permissions().create(
    fileId=spreadsheetId,
    # Открываем доступ на редактирование
    body={'type': 'user', 'role': 'writer', 'emailAddress': 'gavrilovivan2001@gmail.com'},
    fields='id'
).execute()















