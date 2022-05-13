from telebot import types


def money_kinds() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры по методам привлечения денег"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Областное финансирование'))
    keyboard.add(types.KeyboardButton(text='Мне нужны раменские субсидии'))
    keyboard.add(types.KeyboardButton(text='Мне нужен инвестор'))
    keyboard.add(types.KeyboardButton(text='Мне нужен льготный кредит'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_money_kinds() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к способам привлечения денег или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def money_country_finance() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для методов привлечения денег"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Бесплатная печать полиграфии'))
    keyboard.add(types.KeyboardButton(text='Бесплатные видео- и аудиоролики'))
    keyboard.add(types.KeyboardButton(text='Бесплатная наружная реклама'))
    keyboard.add(types.KeyboardButton(text='Бесплатное создание фирменного стиля'))
    keyboard.add(types.KeyboardButton(text='Бесплатное создание сайта'))
    keyboard.add(types.KeyboardButton(text='Софинансирование рекламной компании от Яндекс.Директ'))
    keyboard.add(types.KeyboardButton(text='Софинансирование рекламной компании от Яндекс.Бизнес'))
    keyboard.add(types.KeyboardButton(text='Софинансирование рекламной компании от Яндекс.Карты'))
    keyboard.add(types.KeyboardButton(text='Софинансирование рекламной компании от Яндекс.Взгляд'))
    keyboard.add(types.KeyboardButton(text='Компенсация затрат на оборудование'))
    keyboard.add(types.KeyboardButton(text='Компенсация затрат на социальное предпринимательство'))
    keyboard.add(types.KeyboardButton(text='Компенсация затрат на маркетплейсах'))
    keyboard.add(types.KeyboardButton(text='Лизинг оборудования'))
    keyboard.add(types.KeyboardButton(text='Гранты социальным предприятиям'))
    keyboard.add(types.KeyboardButton(text='Гранты молодым предприятиям'))
    keyboard.add(types.KeyboardButton(text='Компенсация % ставки по кредитам'))
    keyboard.add(types.KeyboardButton(text='Поручительства'))
    keyboard.add(types.KeyboardButton(text='Микрозаймы'))
    keyboard.add(types.KeyboardButton(text='Льгота 50% по аренде'))
    keyboard.add(types.KeyboardButton(text='Компенсация затрат на размещение в коворкинге'))
    keyboard.add(types.KeyboardButton(text='Компенсация расходов на СБП'))
    keyboard.add(types.KeyboardButton(text='Кредитные каникулы'))
    keyboard.add(types.KeyboardButton(text='Субсидии на найм молодых сотрудников'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_money_country_finance() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к способам привлечения денег,
    в главное меню или областному финансированию"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к видам областного финансирования'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def money_need_credit_link() -> types.InlineKeyboardMarkup:
    """Функция для создания инлайн клавиатуры """

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='МКК', url='https://www.mofmicro.ru/ru/'))
    return keyboard


def money_country_advert_link() -> types.InlineKeyboardMarkup:
    """Функция для создания инлайн клавиатуры """

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Подать заявку', url='https://uslugi.mosreg.ru/services/20796'))
    return keyboard


def ramensk_subsidies_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Да'))
    keyboard.add(types.KeyboardButton(text='Нет, я самозанятый'))
    keyboard.add(types.KeyboardButton(text='Нет, но я планирую стать ИП или самозанятым или '
                                           'открыть организацию'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def ramensk_subsidies_IP_yes_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Да, я соответствую'))
    keyboard.add(types.KeyboardButton(text='Нет, я не соответствую'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def ramensk_subsidies_no_1_link() -> types.InlineKeyboardMarkup:
    """Функция для создания инлайн клавиатуры """

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Инвестиционный портал Московской области',
                                            url='https://invest.mosreg.ru/investor/calculator'))
    return keyboard


def back_to_money_ramensk_subsidies() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения в главное меню или раменским субсидиям"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к раменским субсидиям'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def ramensk_subsidies_no_2_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Меньше прожиточного минимума'))
    keyboard.add(types.KeyboardButton(text='Больше прожиточного минимума'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def ramensk_subsidies_kinds_subsidies_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Общая'))
    keyboard.add(types.KeyboardButton(text='Социальная'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к методам привлечения денежных средств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def ramensk_subsidies_social_subsidies_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Да'))
    keyboard.add(types.KeyboardButton(text='Нет'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def what_later_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Отлично, что дальше?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def general_buy_rus_aboard_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='В России'))
    keyboard.add(types.KeyboardButton(text='Зарубежом'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def all_ok_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Всё в порядке, что дальше?'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def all_ok_and_nothing_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Всё в порядке, что дальше?'))
    keyboard.add(types.KeyboardButton(text='Чего-то не хватает'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def general_rus_10_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Для индивидуальных предпринимателей'))
    keyboard.add(types.KeyboardButton(text='Для юридических лиц'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def how_send_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Как отправить документы'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def general_send_advertisement() -> types.InlineKeyboardMarkup:
    """Функция для создания инлайн клавиатуры """

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='ПОДАТЬ ДОКУМЕНТЫ', url='https://uslugi.mosreg.ru/services/21001'))
    return keyboard
