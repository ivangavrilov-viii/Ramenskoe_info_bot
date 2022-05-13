from telebot import types


def promotion_kinds() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры по видам продвижения"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Разместите рекламу на городских рекламных щитах'))
    keyboard.add(types.KeyboardButton(text='Выступите на радио'))
    keyboard.add(types.KeyboardButton(text='Примите участие в городских мероприятиях'))
    keyboard.add(types.KeyboardButton(text='Разместите ссылку о себе в Раменском бизнес-чате'))
    keyboard.add(types.KeyboardButton(text='О вас расскажут СМИ. Именно Ваше мнение будет '
                                           'востребовано на весь регион.'))
    keyboard.add(types.KeyboardButton(text='Продайте товар за рубежом'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_promotion_kinds() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к видам продвижения или в главное меню"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к видам продвижения'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def promotion_kinds_sale_aboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для продажи товара зарубежом"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Софинансирование транспортировки на новые экспортные рынки'))
    keyboard.add(types.KeyboardButton(text='Софинансирование сертификации продукции'))
    keyboard.add(types.KeyboardButton(text='Софинансирование организации международных бизнес-миссий (выставок)'))
    keyboard.add(types.KeyboardButton(text='Создание и модернизация сайта'))
    keyboard.add(types.KeyboardButton(text='Размещение на международных электронных площадках'))
    keyboard.add(types.KeyboardButton(text='Перевод текстов на иностранные языки'))
    keyboard.add(types.KeyboardButton(text='Маркетинговые исследования иностранных рынков'))
    keyboard.add(types.KeyboardButton(text='Поиск зарубежных партнеров'))
    keyboard.add(types.KeyboardButton(text='Участие в международных выставках за рубежом и в РФ'))
    keyboard.add(types.KeyboardButton(text='Патентование продукции'))
    keyboard.add(types.KeyboardButton(text='Обучение в акселерационных программах экспорта'))
    keyboard.add(types.KeyboardButton(text='Семинары, вебинары, круглые столы по экспорту'))
    keyboard.add(types.KeyboardButton(text='Консультации по правовым вопросам, логистике, таможне'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к видам продвижения'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def back_to_sale_aboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к видам продвижения, главное меню или продажам зарубежом"""

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к продажам зарубежом'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к видам продвижения'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def abroad_link() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='Подробнее', url='https://exportmo.ru/service'))
    return keyboard
