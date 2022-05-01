from telebot import types


def lands_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры по поиску земли и помещений"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Установить киоск/павильон/палатку'))
    keyboard.add(types.KeyboardButton(text='Установить иной некапитальный объект'))
    keyboard.add(types.KeyboardButton(text='Установить капитальный объект/строение или вести фермерское хозяйство'))
    keyboard.add(types.KeyboardButton(text='Организовать ярмарку'))
    keyboard.add(types.KeyboardButton(text='Получить помещение'))
    keyboard.add(types.KeyboardButton(text='Продление договора аренды'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def non_capital_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к поиску земли и помещений или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Как получить услугу ?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_lands_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к поиску земли и помещений или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к поиску земли и помещений'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def check_set_up_capital() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Да'))
    keyboard.add(types.KeyboardButton(text='Нет'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к поиску земли и помещений'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def check_set_up_capital_object() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Да'))
    keyboard.add(types.KeyboardButton(text='Нет'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def check_set_up_capital_object_back() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def set_up_kiosk_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Частная земля'))
    keyboard.add(types.KeyboardButton(text='Гос.земля'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def set_up_kiosk_set_up_NTO_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Как сделать презентацию ?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def set_up_kiosk_main_req_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Основные требования по включению НТО в схему?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def set_up_kiosk_auq_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Как принять участие в аукционе?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def land_capital_make_link() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Подать заявку', url='https://uslugi.mosreg.ru/services/16020%20'))
    return keyboard


def land_rent_link() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Подать заявку', url='https://www.gosuslugi.ru/233423'))
    return keyboard


def set_up_kiosk_private_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к поиску земли и помещений или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Как согласовать?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def set_up_kiosk_private_link() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Получить услугу', url='https://uslugi.mosreg.ru/services/21469'))
    return keyboard


def set_up_kiosk_non_capital_link() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Получить услугу',
                                            url='https://uslugi.mosreg.ru/services/11499'))
    return keyboard
