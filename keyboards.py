from telebot import types


def main_aims() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры главного меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Мне нужны деньги'))
    keyboard.add(types.KeyboardButton(text='Мне нужно продвижение'))
    keyboard.add(types.KeyboardButton(text='Мне нужны знакомства'))
    keyboard.add(types.KeyboardButton(text='Мне нужны работники'))
    keyboard.add(types.KeyboardButton(text='Мне нужны земля и помещение'))
    keyboard.add(types.KeyboardButton(text='Другие меры поддержки'))
    return keyboard







def meet_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры по поиску знакомств"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Персональный поиск бизнес-партнеров'))
    keyboard.add(types.KeyboardButton(text='Раменский бизнес-чат'))
    keyboard.add(types.KeyboardButton(text='Участие в городских мероприятиях'))
    keyboard.add(types.KeyboardButton(text='Стать членом бизнес-сообщества'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_meet_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к списку знакомств или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к списку знакомств'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def workers_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры по поиску работников"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Найти в Центре занятости населения'))
    keyboard.add(types.KeyboardButton(text='Найти в Федеральной базе вакансий и резюме'))
    keyboard.add(types.KeyboardButton(text='Привлечь труд осужденных'))
    keyboard.add(types.KeyboardButton(text='Волонтёры на мероприятия'))
    keyboard.add(types.KeyboardButton(text='Подбор участников на мероприятия'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_workers_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к поиску работников или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к поиску работников'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def other_supports_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры по поиску работников"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Бизнес Омбудсмен Раменского г.о.'))
    keyboard.add(types.KeyboardButton(text='Бесплатная юридическая помощь для МСП'))
    keyboard.add(types.KeyboardButton(text='Консультации от Управления потребительского рынка, '
                                           'инвестиций и развития предпринимательства'))
    keyboard.add(types.KeyboardButton(text='Наладить производство'))
    keyboard.add(types.KeyboardButton(text='Наладить фермерское хозяйство'))
    keyboard.add(types.KeyboardButton(text='IT сфера'))
    keyboard.add(types.KeyboardButton(text='Мораторий на проверки'))
    keyboard.add(types.KeyboardButton(text='Продление лицензий'))
    keyboard.add(types.KeyboardButton(text='Образовательные программы и обучающие мероприятия'))
    keyboard.add(types.KeyboardButton(text='Записаться на личный прием'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_other_supports_kind() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к поиску работников или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к мерам поддержки'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard







