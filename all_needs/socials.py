from telebot import types


def socials_kinds_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='На аренду'))
    keyboard.add(types.KeyboardButton(text='На оплату коммунальных услуг'))
    keyboard.add(types.KeyboardButton(text='На выкуп помещения'))
    keyboard.add(types.KeyboardButton(text='На текущий ремонт (осуществляется подрядным или хозяйственным способом)'))
    keyboard.add(types.KeyboardButton(text='На капитальный ремонт'))
    keyboard.add(types.KeyboardButton(text='На реконструкцию помещения'))
    keyboard.add(types.KeyboardButton(text='На затраты по приобретению основных средств (за исключением легковых '
                                           'автотранспортных средств)'))
    keyboard.add(types.KeyboardButton(text='На сырье/расходники'))
    keyboard.add(types.KeyboardButton(text='На участие в региональных, межрегиональных и международных выставочных '
                                           'и выставочно-ярмарочных мероприятий'))
    keyboard.add(types.KeyboardButton(text='На приобретение оборудования'))
    keyboard.add(types.KeyboardButton(text='На повышение квалификации и (или) участие в образовательных программах '
                                           'работников'))
    keyboard.add(types.KeyboardButton(text='На медицинское обслуживание детей'))
    keyboard.add(types.KeyboardButton(text='На приобретение комплектующих изделий'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_all_ok_or_nothing_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Всё в порядке, что дальше?'))
    keyboard.add(types.KeyboardButton(text='Чего-то не хватает'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_all_ok_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Всё в порядке'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_IP_or_entity_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Для индивидуальных предпринимателей'))
    keyboard.add(types.KeyboardButton(text='Для юридических лиц'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_send_doc() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры  """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Как отправить документы'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_send_advertisement() -> types.InlineKeyboardMarkup:
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(text='ПОДАТЬ ДОКУМЕНТЫ', url='https://uslugi.mosreg.ru/services/21001'))
    return keyboard


def socials_finish() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='< Вернуться к раменским субсидиям'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_nal_beznal_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Расчет безналичным способом'))
    keyboard.add(types.KeyboardButton(text='Расчет наличными денежными средствами'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard


def socials_repair_kinds_keyboard() -> types.ReplyKeyboardMarkup:
    """Функция для создания клавиатуры для возвращения к """

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton(text='Подрядный способ (Ремонт подрядной организацией по договору)'))
    keyboard.add(types.KeyboardButton(text='Хозяйственным способом (Ремонт осуществляется своими силами)'))
    keyboard.add(types.KeyboardButton(text='< Назад'))
    keyboard.add(types.KeyboardButton(text='< Вернуться к целям обращения'))
    return keyboard

