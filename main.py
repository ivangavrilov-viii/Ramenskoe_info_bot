from all_needs_messages import meet_mes, money_mes, land_mes, work_mes, prom_mes, other_mes, socials_mes
from all_needs import land, promotion, money, socials
from telebot.types import InputMediaPhoto
from bot_users.class_user import BotUser
from telebot.types import Message
from decouple import config
from typing import Dict
import sheets_example
import keyboards
import datetime
import telebot
import time


bot = telebot.TeleBot(config('Ram2biz_bot'))
users_dict: Dict[int, BotUser] = dict()


@bot.message_handler(content_types=['text'])
def start(message: Message) -> None:
    """Функция вызова и обработки основных команд бота"""

    global users_dict

    if message.text == '/start':
        if message.chat.id not in users_dict:
            users_dict[message.chat.id] = BotUser(message.chat)
        bot.send_message(message.chat.id, start_message(message))
        bot.register_next_step_handler(message, input_inn)
    else:
        if message.chat.id in users_dict:
            if not message.text.startswith('<'):
                users_dict[message.chat.id].bot_way += f'{message.text} -> '

            if message.text == 'Мне нужны деньги':
                users_dict[message.chat.id].start_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
                bot.send_message(message.chat.id, money_mes.choose_money_message(), reply_markup=money.money_kinds())
            elif message.text == 'Мне нужен льготный кредит':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, money_mes.money_need_credit(),
                                 reply_markup=money.money_need_credit_link())
                bot.send_message(message.chat.id, text=back_mes(), reply_markup=money.back_to_money_kinds())
            elif message.text == 'Мне нужен инвестор':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, money_mes.money_need_investor(),
                                 reply_markup=money.back_to_money_kinds())
            elif message.text == 'Областное финансирование':
                bot.send_message(message.chat.id, money_mes.choose_money_message(),
                                 reply_markup=money.money_country_finance())
                bot.register_next_step_handler(message, money_country_finance)
            elif message.text == 'Мне нужны раменские субсидии':
                bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP(),
                                 reply_markup=money.ramensk_subsidies_keyboard())
                bot.register_next_step_handler(message, money_ramensk_subsidies)
            elif message.text == '< Вернуться к раменским субсидиям':
                bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP(),
                                 reply_markup=money.ramensk_subsidies_keyboard())
                bot.register_next_step_handler(message, money_ramensk_subsidies)
            elif message.text == '< Вернуться к методам привлечения денежных средств':
                bot.send_message(message.chat.id, money_mes.choose_money_message(), reply_markup=money.money_kinds())
            elif message.text == '< Вернуться к видам областного финансирования':
                bot.send_message(message.chat.id, money_mes.choose_money_message(),
                                 reply_markup=money.money_country_finance())
                bot.register_next_step_handler(message, money_country_finance)

            elif message.text == 'Мне нужно продвижение':
                users_dict[message.chat.id].start_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
                bot.send_message(message.chat.id, prom_mes.choose_promotion_message(),
                                 reply_markup=promotion.promotion_kinds())
            elif message.text == 'Разместите рекламу на городских рекламных щитах':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, prom_mes.billboard_advertising(),
                                 reply_markup=promotion.back_to_promotion_kinds())
            elif message.text == 'Выступите на радио':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, prom_mes.radio(), reply_markup=promotion.back_to_promotion_kinds())
            elif message.text == 'Примите участие в городских мероприятиях':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, prom_mes.city_events(),
                                 reply_markup=promotion.back_to_promotion_kinds())
            elif message.text == 'Разместите ссылку о себе в Раменском бизнес-чате':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, prom_mes.business_chat(),
                                 reply_markup=promotion.back_to_promotion_kinds())
            elif message.text == 'О вас расскажут СМИ. Именно Ваше мнение будет ' \
                                 'востребовано на весь регион.':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, prom_mes.media(), reply_markup=promotion.back_to_promotion_kinds())
            elif message.text == 'Продайте товар за рубежом':
                bot.send_message(message.chat.id, prom_mes.choose_promotion_message(),
                                 reply_markup=promotion.promotion_kinds_sale_aboard())
                bot.register_next_step_handler(message, promotion_sale_aboard)
            elif message.text == '< Вернуться к продажам зарубежом':
                bot.send_message(message.chat.id, prom_mes.choose_promotion_message(),
                                 reply_markup=promotion.promotion_kinds_sale_aboard())
                bot.register_next_step_handler(message, promotion_sale_aboard)
            elif message.text == '< Вернуться к видам продвижения':
                bot.send_message(message.chat.id, prom_mes.choose_promotion_message(),
                                 reply_markup=promotion.promotion_kinds())

            elif message.text == 'Мне нужны знакомства':
                users_dict[message.chat.id].start_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
                bot.send_message(message.chat.id, meet_mes.choose_meet_message(), reply_markup=keyboards.meet_kind())
            elif message.text == 'Персональный поиск бизнес-партнеров':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, meet_mes.partner_search(), reply_markup=keyboards.back_to_meet_kind())
            elif message.text == 'Раменский бизнес-чат':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, meet_mes.business_chat(), reply_markup=keyboards.back_to_meet_kind())
            elif message.text == 'Участие в городских мероприятиях':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, meet_mes.city_events(), reply_markup=keyboards.back_to_meet_kind())
            elif message.text == 'Стать членом бизнес-сообщества':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, meet_mes.business_community_1())
                bot.send_message(message.chat.id, meet_mes.business_community_2())
                bot.send_message(message.chat.id, meet_mes.business_community_3())
                bot.send_message(message.chat.id, meet_mes.business_community_4(),
                                 reply_markup=keyboards.back_to_meet_kind())
            elif message.text == '< Вернуться к списку знакомств':
                bot.send_message(message.chat.id, meet_mes.choose_meet_message(), reply_markup=keyboards.meet_kind())

            elif message.text == 'Мне нужны работники':
                users_dict[message.chat.id].start_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
                bot.send_message(message.chat.id, work_mes.choose_workers_message(),
                                 reply_markup=keyboards.workers_kind())
            elif message.text == 'Найти в Центре занятости населения':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, work_mes.employment_center(),
                                 reply_markup=keyboards.back_to_workers_kind())
            elif message.text == 'Найти в Федеральной базе вакансий и резюме':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, work_mes.federal_base(),
                                 reply_markup=keyboards.back_to_workers_kind())
            elif message.text == 'Привлечь труд осужденных':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, work_mes.convict_labor())
                bot.send_message(message.chat.id, work_mes.workers_call(),
                                 reply_markup=keyboards.back_to_workers_kind())
            elif message.text == 'Волонтёры на мероприятия':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, work_mes.workers_call(),
                                 reply_markup=keyboards.back_to_workers_kind())
            elif message.text == 'Подбор участников на мероприятия':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, work_mes.workers_call(),
                                 reply_markup=keyboards.back_to_workers_kind())
            elif message.text == '< Вернуться к поиску работников':
                bot.send_message(message.chat.id, work_mes.choose_workers_message(),
                                 reply_markup=keyboards.workers_kind())

            elif message.text == 'Мне нужны земля и помещение':
                users_dict[message.chat.id].start_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
                bot.send_message(message.chat.id, land_mes.choose_land_message(), reply_markup=land.lands_kind())
            elif message.text == 'Установить киоск/павильон/палатку':
                bot.send_message(message.chat.id, text='Выберете: ', reply_markup=land.set_up_kiosk_keyboard())
                bot.register_next_step_handler(message, land_set_up_kiosk)
            elif message.text == 'Установить иной некапитальный объект':
                bot.send_message(message.chat.id, land_mes.non_capital_object_1(),
                                 reply_markup=land.non_capital_keyboard())
                bot.register_next_step_handler(message, land_set_up_kiosk_non_capital)
            elif message.text == 'Установить капитальный объект/строение или вести фермерское хозяйство':
                bot.send_message(message.chat.id, land_mes.capital_object(),
                                 reply_markup=land.check_set_up_capital_object())
                bot.register_next_step_handler(message, land_check_capital)
            elif message.text == 'Организовать ярмарку':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, land_mes.organize_fair())
                bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
            elif message.text == 'Получить помещение':
                write_in_table(users_dict[message.chat.id])
                media_group = []
                for num in range(1, 11):
                    media_group.append(InputMediaPhoto(open('area_photos_land/%d.jpg' % num, 'rb')))
                bot.send_media_group(message.chat.id, media=media_group)
                bot.send_message(message.chat.id, land_mes.get_premises())
                bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
            elif message.text == 'Продление договора аренды':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, land_mes.renewal_of_lease(), reply_markup=land.land_rent_link())
                bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
            elif message.text == '< Вернуться к поиску земли и помещений':
                bot.send_message(message.chat.id, other_mes.choose_other_supports_message(),
                                 reply_markup=land.lands_kind())

            elif message.text == 'Другие меры поддержки':
                users_dict[message.chat.id].start_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
                bot.send_message(message.chat.id, other_mes.choose_other_supports_message(),
                                 reply_markup=keyboards.other_supports_kind())
            elif message.text == 'Бизнес Омбудсмен Раменского г.о.':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.ombudsment(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Бесплатная юридическая помощь для МСП':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.free_legal_consult(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Консультации от Управления потребрынка, инвестиций и предпринимательства':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.consult_control(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Наладить производство':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.set_up_production(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Наладить фермерское хозяйство':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.set_up_ferm(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'IT сфера':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.it_area(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Мораторий на проверки':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.moratorium_on_inspections(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Продление лицензий':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.license_renewal(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Образовательные программы и обучающие мероприятия':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.educational_programs_1())
                bot.send_message(message.chat.id, other_mes.educational_programs_2(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == 'Записаться на личный прием':
                write_in_table(users_dict[message.chat.id])
                bot.send_message(message.chat.id, other_mes.make_an_appointment(),
                                 reply_markup=keyboards.back_to_other_supports_kind())
            elif message.text == '< Вернуться к мерам поддержки':
                bot.send_message(message.chat.id, other_mes.choose_other_supports_message(),
                                 reply_markup=keyboards.other_supports_kind())
            elif message.text == '< Вернуться к целям обращения':
                bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
            else:
                bot.send_message(message.chat.id, error_mes(), reply_markup=keyboards.main_aims())
                bot.register_next_step_handler(message, start)
        else:
            users_dict[message.chat.id] = BotUser(message.chat)
            bot.send_message(message.chat.id, start_message(message))
            bot.register_next_step_handler(message, input_inn)


def write_in_table(user: BotUser) -> None:
    user.end_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
    sheets_example.insert_values(user.insert_in_table())
    user.bot_way = ''
    user.start_time = None
    user.end_time = None


def input_inn(message: Message) -> None:
    user_inn = message.text
    user_id = message.chat.id
    error = False

    if user_inn.isdigit() and (len(user_inn) == 12 or len(user_inn) == 10):
        users_dict[user_id].inn = user_inn
        bot.send_message(user_id, phone_message())
        bot.register_next_step_handler(message, input_phone)
    else:
        error = True

    if error:
        bot.send_message(user_id, 'Введен неправильный ИНН...\nПопробуйте ввести снова')
        bot.register_next_step_handler(message, input_inn)


def input_phone(message: Message) -> None:
    user_id = message.chat.id
    user_phone = message.text
    user_phone_list = list(message.text)
    error = False

    if len(user_phone_list) == 12:
        if user_phone_list[0] == '+' and user_phone_list[1] == '7':
            for symbol in user_phone_list[2:]:
                if not symbol.isdigit():
                    error = True
        else:
            error = True
    elif len(user_phone_list) == 11:
        if user_phone_list[0] == '8':
            for symbol in user_phone_list[1:]:
                if not symbol.isdigit():
                    error = True
        else:
            error = True
    else:
        error = True

    if error:
        bot.send_message(user_id, 'Введен неправильный номер телефона...\nПопробуйте ввести заново\n\n'
                                  'Но уже в формате +7ХХХХХХХХХХ или 8XXXXXXXXXX')
        bot.register_next_step_handler(message, input_phone)
    else:
        users_dict[user_id].phone = user_phone
        bot.send_message(user_id, choose_service_message(), reply_markup=keyboards.main_aims())


# !!! ЗАПИСЬ В ТАБЛИЦУ  !!!
def land_check_capital(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Да':
        users_dict[message.chat.id].bot_way += 'Входит в перечень импортозамещения'
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, land_mes.check_capital_true_message_1(),
                         reply_markup=land.land_rent_link())
        bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == 'Нет':
        users_dict[message.chat.id].bot_way += ' Не входит в перечень импортозамещения'
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, 'Выберете участок:\nНемного подождите пока загрузятся файлы...')
        file_1 = open('info_materials/Промышленные земельные объекты.pptx', 'rb')
        file_2 = open('info_materials/Сельско-хозяйственные земельные объекты.pptx', 'rb')
        try:
            bot.send_document(message.chat.id, file_1)
            bot.send_document(message.chat.id, file_2)
            bot.send_message(message.chat.id, text='Объем инвестиций более 50 млн.руб ?',
                             reply_markup=land.check_set_up_capital_object())
            bot.register_next_step_handler(message, land_check_capital_false)
        except Exception as exception:
            print(f'{exception}')
            bot.send_message(message.chat.id, 'Извините, проблемы на сервере...\nПопробуйте позже')
            bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
            bot.register_next_step_handler(message, start)
        file_1.close()
        file_2.close()
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, land_mes.choose_land_message(), reply_markup=land.lands_kind())
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.check_set_up_capital_object())
        bot.register_next_step_handler(message, land_check_capital)


def land_check_capital_false(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Да':
        bot.send_message(message.chat.id, land_mes.check_capital_true_message_true())
        bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == 'Нет':
        bot.send_message(message.chat.id, land_mes.check_capital_true_message_false())
        bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, land_mes.capital_object(), reply_markup=land.check_set_up_capital_object())
        bot.register_next_step_handler(message, land_check_capital)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.check_set_up_capital_object())
        bot.register_next_step_handler(message, land_check_capital_false)


# !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def land_set_up_kiosk(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Частная земля':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, land_mes.check_set_up_kiosk_private_1(),
                         reply_markup=land.set_up_kiosk_private_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_private)
    elif user_answer == 'Гос.земля':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])

        file = open('info_materials/Как установить Нестационарный Торговый Объект.pdf', 'rb')
        bot.send_message(message.chat.id, 'Как установить НТО в Раменском г.о.\nПодождите пока загрузится файл...')
        try:
            bot.send_document(message.chat.id, file)
            time.sleep(1)
            bot.send_message(message.chat.id, 'Нажмите кнопку на клавиатуре: ',
                             reply_markup=land.set_up_kiosk_set_up_NTO_keyboard())
            bot.register_next_step_handler(message, land_set_up_kiosk_prezent)
        except Exception as exception:
            print(exception)
            bot.send_message(message.chat.id, 'Извините, проблемы на сервере...\nПопробуйте позже')
            bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
            bot.register_next_step_handler(message, start)
        file.close()
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, land_mes.choose_land_message(), reply_markup=land.lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.set_up_kiosk_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk)


def land_set_up_kiosk_private(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как согласовать?':
        bot.send_message(message.chat.id, land_mes.check_set_up_kiosk_private_2(),
                         reply_markup=land.set_up_kiosk_private_link())
        bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='Выберете: ', reply_markup=land.set_up_kiosk_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.set_up_kiosk_private_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_private)


def land_set_up_kiosk_prezent(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как сделать презентацию ?':
        file = open('info_materials/Презентация МВК Раменское для примера.pptx', 'rb')
        try:
            bot.send_document(message.chat.id, file)
            time.sleep(1)
            bot.send_message(message.chat.id, 'Нажмите кнопку на клавиатуре: ',
                             reply_markup=land.set_up_kiosk_main_req_keyboard())
            bot.register_next_step_handler(message, land_set_up_kiosk_req)
        except Exception as exception:
            print(exception)
            bot.send_message(message.chat.id, 'Извините, проблемы на сервере...\nПопробуйте позже')
            bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
            bot.register_next_step_handler(message, start)
        file.close()
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='Выберете: ', reply_markup=land.set_up_kiosk_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.set_up_kiosk_set_up_NTO_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_prezent)


def land_set_up_kiosk_req(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Основные требования по включению НТО в схему?':
        file = open('info_materials/Основные требования по включению НТО.jpg', 'rb')
        try:
            bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, 'Нажмите кнопку на клавиатуре: ',
                             reply_markup=land.set_up_kiosk_auq_keyboard())
            bot.register_next_step_handler(message, land_set_up_kiosk_finish)
        except Exception as exception:
            print(exception)
            bot.send_message(message.chat.id, 'Извините, проблемы на сервере...\nПопробуйте позже')
            bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
            bot.register_next_step_handler(message, start)
        file.close()
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Как установить НТО в Раменском г.о.\nПодождите пока загрузится файл...')
        bot.send_document(message.chat.id,
                          open('info_materials/Как установить Нестационарный Торговый Объект.pdf', 'rb'))
        time.sleep(2)
        bot.send_message(message.chat.id, 'Нажмите кнопку на клавиатуре',
                         reply_markup=land.set_up_kiosk_set_up_NTO_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_prezent)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.set_up_kiosk_main_req_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_req)


def land_set_up_kiosk_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как принять участие в аукционе?':
        file = open('info_materials/Как принять участие в аукционе на НТО.jpg', 'rb')
        try:
            bot.send_document(message.chat.id, file)
            bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                             reply_markup=land.back_to_lands_kind())
            bot.register_next_step_handler(message, start)
        except Exception as exception:
            print(exception)
            bot.send_message(message.chat.id, 'Извините, проблемы на сервере...\nПопробуйте позже')
            bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
            bot.register_next_step_handler(message, start)
        file.close()
    elif user_answer == '< Назад':
        bot.send_document(message.chat.id, open('info_materials/Презентация МВК Раменское для примера.pptx', 'rb'))
        bot.send_message(message.chat.id, 'Нажмите кнопку на клавиатуре: ',
                         reply_markup=land.set_up_kiosk_main_req_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_req)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.set_up_kiosk_auq_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_finish)


# !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def land_set_up_kiosk_non_capital(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как получить услугу ?':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, land_mes.non_capital_object_2(),
                         reply_markup=land.set_up_kiosk_non_capital_link())
        bot.send_message(message.chat.id, back_mes(), reply_markup=land.back_to_lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, land_mes.choose_land_message(), reply_markup=land.lands_kind())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=land.non_capital_keyboard())
        bot.register_next_step_handler(message, land_set_up_kiosk_non_capital)


#  !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def promotion_sale_aboard(message: Message) -> None:
    """Функция обработки всех запросов по 'Мне нужно продвижение' -> 'Продайте товар за рубежом' """

    sale_aboard_user_answer = message.text
    if sale_aboard_user_answer == 'Софинансирование транспортировки на новые экспортные рынки':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_1(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Софинансирование сертификации продукции':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_2(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Софинансирование организации международных бизнес-миссий (выставок)':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_3(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Создание и модернизация сайта':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_4(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Размещение на международных электронных площадках':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_5(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Перевод текстов на иностранные языки':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_6(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Маркетинговые исследования иностранных рынков':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_7(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Поиск зарубежных партнеров':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_8(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Участие в международных выставках за рубежом и в РФ':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_9(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Патентование продукции':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_10(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Обучение в акселерационных программах экспорта':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_11(), reply_markup=promotion.abroad_link())
        bot.send_message(message.chat.id, text=back_mes(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Семинары, вебинары, круглые столы по экспорту':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_more(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == 'Консультации по правовым вопросам, логистике, таможне':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, prom_mes.sale_abroad_more(), reply_markup=promotion.back_to_sale_aboard())
    elif sale_aboard_user_answer == '< Вернуться к видам продвижения':
        bot.send_message(message.chat.id, prom_mes.choose_promotion_message(), reply_markup=promotion.promotion_kinds())
        bot.register_next_step_handler(message, start)
    elif sale_aboard_user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=promotion.promotion_kinds_sale_aboard())
        bot.register_next_step_handler(message, promotion_sale_aboard)


#  !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def money_country_finance(message: Message) -> None:
    """Функция обработки всех запросов по 'Мне нужны деньги' -> 'Областное финансирование' """

    country_finance_user_answer = message.text
    if country_finance_user_answer == 'Бесплатная печать полиграфии':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_print(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Бесплатные видео- и аудиоролики':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_free_audio(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Бесплатная наружная реклама':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_free_advertising(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Бесплатное создание фирменного стиля':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_firm_style(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Бесплатное создание сайта':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_website(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Софинансирование рекламной компании от Яндекс.Директ':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_yandex_direct(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Софинансирование рекламной компании от Яндекс.Бизнес':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_yandex_business(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Софинансирование рекламной компании от Яндекс.Карты':
        users_dict[message.chat.id].bot_way += f'{message.text}'
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_yandex_maps(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Софинансирование рекламной компании от Яндекс.Взгляд':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_yandex_view(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Компенсация затрат на оборудование':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_equipment_compensation(),
                         reply_markup=money.money_country_advert_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Компенсация затрат на социальное предпринимательство':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_social_compensation(),
                         reply_markup=money.money_country_advert_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Компенсация затрат на маркетплейсах':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_marketplace_compensation(),
                         reply_markup=money.money_country_advert_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Лизинг оборудования':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_lizing(),
                         reply_markup=money.money_country_advert_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Гранты социальным предприятиям':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_grants_social(),
                         reply_markup=money.money_country_advert_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Гранты молодым предприятиям':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_grants_young(),
                         reply_markup=money.money_country_advert_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Компенсация % ставки по кредитам':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_credits_compensation(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Поручительства':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_guarantees(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Микрозаймы':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_microloans(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Льгота 50% по аренде':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_rental_allowance(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Компенсация затрат на размещение в коворкинге':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_accomodation(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Компенсация расходов на СБП':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_SBP(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Кредитные каникулы':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_credits_holidays(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == 'Субсидии на найм молодых сотрудников':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_county_finance_young_worker(),
                         reply_markup=money.back_to_money_country_finance())
    elif country_finance_user_answer == '< Вернуться к методам привлечения денежных средств':
        bot.send_message(message.chat.id, money_mes.choose_money_message(), reply_markup=money.money_kinds())
        bot.register_next_step_handler(message, start)
    elif country_finance_user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.money_country_finance())
        bot.register_next_step_handler(message, money_country_finance)


#  !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def money_ramensk_subsidies(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Да':
        users_dict[message.chat.id].bot_way += f'ИП или Юр. лицо -> '
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_yes(),
                         reply_markup=money.ramensk_subsidies_IP_yes_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_yes)
    elif user_answer == 'Нет, я самозанятый':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == 'Нет, но я планирую стать ИП или самозанятым или ' \
                        'открыть организацию':
        users_dict[message.chat.id].bot_way += f'{message.text} -> '
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_2(),
                         reply_markup=money.ramensk_subsidies_no_2_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_no_but)
    elif user_answer == '< Вернуться к методам привлечения денежных средств':
        bot.send_message(message.chat.id, money_mes.choose_money_message(), reply_markup=money.money_kinds())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.ramensk_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies)


#  !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def money_ramensk_subsidies_no_but(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Меньше прожиточного минимума':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_but_less(),
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == 'Больше прожиточного минимума':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_but_more(),
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Вернуться к методам привлечения денежных средств':
        bot.send_message(message.chat.id, money_mes.choose_money_message(),
                         reply_markup=money.money_kinds())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.ramensk_subsidies_no_2_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_no_but)


def money_ramensk_subsidies_yes(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Да, я соответствую':
        users_dict[message.chat.id].bot_way += f'{message.text} -> '
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_kinds_subsidies(),
                         reply_markup=money.ramensk_subsidies_kinds_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_kinds)
    elif user_answer == 'Нет, я не соответствую':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Вернуться к методам привлечения денежных средств':
        bot.send_message(message.chat.id, money_mes.choose_money_message(), reply_markup=money.money_kinds())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.ramensk_subsidies_IP_yes_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_yes)


def money_ramensk_subsidies_kinds(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Общая':
        users_dict[message.chat.id].bot_way += f'{message.text} -> '
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_general_subsidies(),
                         reply_markup=money.ramensk_subsidies_social_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_general)
    elif user_answer == 'Социальная':
        users_dict[message.chat.id].bot_way += f'{message.text} -> '
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_social_subsidies(),
                         reply_markup=money.ramensk_subsidies_social_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_social)
    elif user_answer == '< Вернуться к методам привлечения денежных средств':
        bot.send_message(message.chat.id, money_mes.choose_money_message(), reply_markup=money.money_kinds())
        bot.register_next_step_handler(message, start)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.ramensk_subsidies_kinds_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_kinds)


#  !!! ЗАПИСЬ В ТАБЛИЦУ !!!
# ВИДЫ ОБЩИХ СУБСИДИЙ
def money_ramensk_subsidies_general(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Да':
        users_dict[message.chat.id].bot_way += f'Веду деятельность по одному из критериев -> '
        bot.send_message(message.chat.id, money_mes.general_yes(), reply_markup=money.what_later_keyboard())
        bot.register_next_step_handler(message, general_yes)
    elif user_answer == 'Нет':
        users_dict[message.chat.id].bot_way += f'Не веду деятельность ни по одному из критериев '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_kinds_subsidies(),
                         reply_markup=money.ramensk_subsidies_kinds_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.ramensk_subsidies_social_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_general)


def general_yes(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Отлично, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_yes_buy(),
                         reply_markup=money.general_buy_rus_aboard_keyboard())
        bot.register_next_step_handler(message, general_yes_2)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_general_subsidies(),
                         reply_markup=money.ramensk_subsidies_social_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_general)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.what_later_keyboard())
        bot.register_next_step_handler(message, general_yes)


#  !!! ЗАПИСЬ В ТАБЛИЦУ !!!
def general_yes_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'В России':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.general_yes_buy_rus(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_1)
    elif user_answer == 'Зарубежом':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, money_mes.general_yes_buy_aboard(), reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_1)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_yes(), reply_markup=money.what_later_keyboard())
        bot.register_next_step_handler(message, general_yes)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.general_buy_rus_aboard_keyboard())
        bot.register_next_step_handler(message, general_yes_2)


def general_abroad_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_1(), reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_yes_buy(),
                         reply_markup=money.general_buy_rus_aboard_keyboard())
        bot.register_next_step_handler(message, general_yes_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_1)


def general_abroad_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_aboard_2(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_3)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_yes_buy_aboard(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_2)


def general_abroad_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_3(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_4)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_1(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_3)


def general_abroad_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_4(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_5)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_aboard_2(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_4)


def general_abroad_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_5(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_6)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_3(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_5)


def general_abroad_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_aboard_6(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_7)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_4(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_6)


def general_abroad_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_7(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_8)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_5(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_7)


def general_abroad_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_8(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_9)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_aboard_6(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_8)


def general_abroad_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_9(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_10)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_7(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_9)


def general_abroad_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_10(),
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_or_entity)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_8(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_10)


def general_abroad_IP_or_entity(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_11(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_12)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_11())
        bot.send_message(message.chat.id, money_mes.general_rus_entity_12(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_9(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_abroad_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_or_entity)


def general_abroad_IP_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_12(),
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_10(),
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_or_entity)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_12)


def general_abroad_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_13(),
                         reply_markup=money.general_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_11(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_finish)


def general_abroad_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_13(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_10(),
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_abroad_IP_or_entity)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_12)


def general_abroad_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_14(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_14)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_12(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_13)


def general_abroad_entity_14(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_15(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_15)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_13(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_14)


def general_abroad_entity_15(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_16(),
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_14(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_14)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_15)


def general_abroad_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_17(),
                         reply_markup=money.general_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_15(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_15)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_abroad_entity_finish)


def general_russia_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_1(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_yes_buy(),
                         reply_markup=money.general_buy_rus_aboard_keyboard())
        bot.register_next_step_handler(message, general_yes_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_1)


def general_russia_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_2(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_3)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_yes_buy_rus(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_2)


def general_russia_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_3(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_4)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_1(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_3)


def general_russia_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_4(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_5)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_2(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_4)


def general_russia_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_5(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_6)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_3(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_5)


def general_russia_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_6(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_7)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_4(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_6)


def general_russia_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_7(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_8)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_5(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_7)


def general_russia_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_8(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_9)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_6(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_8)


def general_russia_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_9(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_10)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_7(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_9)


def general_russia_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_10(),
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_or_entity)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_8(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_10)


def general_russia_IP_or_entity(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_11(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_12)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_11())
        bot.send_message(message.chat.id, money_mes.general_rus_entity_12(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_9(),
                         reply_markup=money.all_ok_and_nothing_keyboard())
        bot.register_next_step_handler(message, general_russia_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_or_entity)


def general_russia_IP_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_12(),
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_10(),
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_or_entity)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_12)


def general_russia_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_13(),
                         reply_markup=money.general_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_IP_11(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_finish)


def general_russia_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_13(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_10(),
                         reply_markup=money.general_rus_10_keyboard())
        bot.register_next_step_handler(message, general_russia_IP_or_entity)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_12)


def general_russia_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_14(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_14)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_12(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_13)


def general_russia_entity_14(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_15(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_15)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_13(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_14)


def general_russia_entity_15(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_16(),
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_14(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_14)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_15)


def general_russia_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_17(),
                         reply_markup=money.general_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.general_rus_entity_15(),
                         reply_markup=money.all_ok_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_15)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете услугу из списка: ',
                         reply_markup=money.how_send_keyboard())
        bot.register_next_step_handler(message, general_russia_entity_finish)


def money_ramensk_subsidies_social(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Да':
        users_dict[message.chat.id].bot_way += f'Попадаю по соц. субсидии ->'
        bot.send_message(message.chat.id, socials_mes.socials_yes_1())
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == 'Нет':
        users_dict[message.chat.id].bot_way += f'{message.text}'
        users_dict[message.chat.id].end_time = datetime.datetime.now().strftime(f'%d-%m-%Y %H:%M:%S')
        sheets_example.insert_values(users_dict[message.chat.id].insert_in_table())
        users_dict[message.chat.id].bot_way = ''
        users_dict[message.chat.id].start_time = None
        users_dict[message.chat.id].end_time = None
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_kinds_subsidies(),
                         reply_markup=money.ramensk_subsidies_kinds_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=money.ramensk_subsidies_social_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_social)


# !!! ЗАПИСЬ В ТАБЛИЦУ !!!
# ВИДЫ СОЦИАЛЬНЫХ СУБСИДИЙ
def socials_kinds(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'На аренду':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_rent_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_rent_1)
    elif user_answer == 'На оплату коммунальных услуг':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_utilities_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_utilities_1)
    elif user_answer == 'На выкуп помещения':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_ransom_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_ransom_1)
    elif user_answer == 'На текущий ремонт (подрядным или хозяйственным)':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, 'Выберете способ осуществления ремонта: ',
                         reply_markup=socials.socials_repair_kinds_keyboard())
        bot.register_next_step_handler(message, socials_repair_choose_kinds)
    elif user_answer == 'На капитальный ремонт':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_1)
    elif user_answer == 'На реконструкцию помещения':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_1)
    elif user_answer == 'На затраты по приобретению основных средств (кроме легкового авто)':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_funds_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_funds_1)
    elif user_answer == 'На сырье/расходники':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_raw_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_raw_1)
    elif user_answer == 'На участие в выставочно-ярмарочных мероприятиях':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_participation_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_1)
    elif user_answer == 'На приобретение оборудования':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_equipment_1_1())
        bot.send_message(message.chat.id, socials_mes.socials_equipment_1_2(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_1)
    elif user_answer == 'На повышение квалификации и (или) участие в образовательных программах работников':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_high_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_1)
    elif user_answer == 'На медицинское обслуживание детей':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_med_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_1)
    elif user_answer == 'На приобретение комплектующих изделий':
        users_dict[message.chat.id].bot_way += f'{message.text} '
        write_in_table(users_dict[message.chat.id])
        bot.send_message(message.chat.id, socials_mes.socials_components_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_components_1)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_social_subsidies(),
                         reply_markup=money.ramensk_subsidies_social_subsidies_keyboard())
        bot.register_next_step_handler(message, money_ramensk_subsidies_social)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)


# НА ТЕКУЩИЙ РЕМОНТ
def socials_repair_choose_kinds(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Подрядный способ (Ремонт подрядной организацией по договору)':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_1)
    elif user_answer == 'Хозяйственным способом (Ремонт осуществляется своими силами)':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_1)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, wrong(), reply_markup=socials.socials_repair_kinds_keyboard())
        bot.register_next_step_handler(message, socials_repair_choose_kinds)


# ПОДРЯДНЫЙ СПОСОБ
def socials_repair_podryd_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберете способ осуществления ремонта: ',
                         reply_markup=socials.socials_repair_kinds_keyboard())
        bot.register_next_step_handler(message, socials_repair_choose_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_1)


def socials_repair_podryd_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_2)


def socials_repair_podryd_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_3)


def socials_repair_podryd_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_4)


def socials_repair_podryd_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_5)


def socials_repair_podryd_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_6)


def socials_repair_podryd_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_7)


def socials_repair_podryd_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_9)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_8)


def socials_repair_podryd_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_IP_10)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_9)


def socials_repair_podryd_IP_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_podryd_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_IP_10)


def socials_repair_podryd_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_IP_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_podryd_IP_finish)


def socials_repair_podryd_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_10)


def socials_repair_podryd_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_11)


def socials_repair_podryd_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_12)


def socials_repair_podryd_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_13)


def socials_repair_podryd_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_podryd_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_podryd_entity_finish)


# ХОЗЯЙСТВЕННЫЙ СПОСОБ
def socials_repair_economic_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберете способ осуществления ремонта: ',
                         reply_markup=socials.socials_repair_kinds_keyboard())
        bot.register_next_step_handler(message, socials_repair_choose_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_1)


def socials_repair_economic_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_2)


def socials_repair_economic_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_3)


def socials_repair_economic_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_4)


def socials_repair_economic_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_5)


def socials_repair_economic_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_calculation)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_6)


def socials_repair_economic_calculation(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Расчет безналичным способом':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_7)
    elif user_answer == 'Расчет наличными денежными средствами':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_calculation)


# БЕЗНАЛИЧНЫЙ РАСЧЕТ
def socials_repair_economic_beznal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_7)


def socials_repair_economic_beznal_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_9(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_8)


def socials_repair_economic_beznal_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_10(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_10)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_9)


def socials_repair_economic_beznal_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_IP_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_IP_11)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_11_1())
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_11_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_9(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_10)


def socials_repair_economic_beznal_IP_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_10(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_IP_11)


def socials_repair_economic_beznal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_IP_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_IP_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_IP_finish)


def socials_repair_economic_beznal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_10(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_11)


def socials_repair_economic_beznal_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_11_1())
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_11_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_12)


def socials_repair_economic_beznal_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_14(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_14)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_13)


def socials_repair_economic_beznal_entity_14(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_14)


def socials_repair_economic_beznal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_beznal_entity_14(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_14)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_beznal_entity_finish)


# НАЛИЧНЫЙ РАСЧЕТ
def socials_repair_economic_nal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_8)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_7)


def socials_repair_economic_nal_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_IP_9)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_8)


def socials_repair_economic_nal_IP_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_nal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_IP_9)


def socials_repair_economic_nal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_IP_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_nal_IP_finish)


def socials_repair_economic_nal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_9)


def socials_repair_economic_nal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_10)


def socials_repair_economic_nal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_11)


def socials_repair_economic_nal_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_12)


def socials_repair_economic_nal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_repair_economic_nal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_repair_economic_nal_entity_finish)


# НА УЧАСТИЕ В РЕГИОНАЛЬНЫХ, межрегиональных и международных выставочных и выставочно-ярмарочных мероприятий
def socials_participation_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_participation_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_1)


def socials_participation_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_3)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_2)


def socials_participation_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_participation_calculation)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_3)


def socials_participation_calculation(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Расчет безналичным способом':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_4)
    elif user_answer == 'Расчет наличными денежными средствами':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_3(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_participation_calculation)


# БЕЗНАЛИЧНЫЙ РАСЧЕТ
def socials_participation_beznal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_participation_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_4)


def socials_participation_beznal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_6(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_5)


def socials_participation_beznal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_7)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_6)
        

def socials_participation_beznal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_IP_8)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_6(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_7)


def socials_participation_beznal_IP_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_beznal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_IP_8)


def socials_participation_beznal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_IP_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_beznal_IP_finish)


def socials_participation_beznal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_8)


def socials_participation_beznal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_9)


def socials_participation_beznal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_10)


def socials_participation_beznal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_11)


def socials_participation_beznal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_beznal_entity_finish)


# НАЛИЧНЫЙ РАСЧЕТ
def socials_participation_nal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_5(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_5)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_participation_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_4)


def socials_participation_nal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_IP_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_IP_7)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_7_1())
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_7_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_6)


def socials_participation_nal_IP_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_nal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_5(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_IP_7)


def socials_participation_nal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_IP_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_IP_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_nal_IP_finish)


def socials_participation_nal_entity_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_5(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_7)


def socials_participation_nal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_7_1())
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_7_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_8)


def socials_participation_nal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_9)


def socials_participation_nal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_nal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_10)


def socials_participation_nal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_participation_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_participation_nal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_participation_nal_entity_finish)


# НА ПРИОБРЕТЕНИЕ ОБОРУДОВАНИЯ
def socials_equipment_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_equipment_calculation)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_1)


def socials_equipment_calculation(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Расчет безналичным способом':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_2)
    elif user_answer == 'Расчет наличными денежными средствами':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_2)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_1_1())
        bot.send_message(message.chat.id, socials_mes.socials_equipment_1_2(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_equipment_calculation)


# БЕЗНАЛИЧНЫЙ РАСЧЕТ
def socials_equipment_beznal_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_equipment_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_2)


def socials_equipment_beznal_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_3)


def socials_equipment_beznal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_4)


def socials_equipment_beznal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_5)


def socials_equipment_beznal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_6)


def socials_equipment_beznal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_8)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_7)


def socials_equipment_beznal_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_IP_9)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_9)


def socials_equipment_beznal_IP_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_beznal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_IP_9)


def socials_equipment_beznal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_IP_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_beznal_IP_finish)


def socials_equipment_beznal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_10)


def socials_equipment_beznal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_10)


def socials_equipment_beznal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_11)


def socials_equipment_beznal_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_12)


def socials_equipment_beznal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_beznal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_beznal_entity_finish)


# НАЛИЧНЫЙ РАСЧЕТ
def socials_equipment_nal_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_3)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_equipment_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_2)


def socials_equipment_nal_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_3)


def socials_equipment_nal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_5(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_4)


def socials_equipment_nal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_6(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_6)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_5)


def socials_equipment_nal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_IP_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_IP_7)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_7_1())
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_7_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_6)


def socials_equipment_nal_IP_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_nal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_6(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_IP_7)


def socials_equipment_nal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_IP_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_IP_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_nal_IP_finish)


def socials_equipment_nal_entity_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_6(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_7)


def socials_equipment_nal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_7_1())
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_7_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_8)


def socials_equipment_nal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_9)


def socials_equipment_nal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_10)


def socials_equipment_nal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_equipment_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_equipment_nal_entity_finish)


# На ЗАТРАТЫ СЫРЬЕ/РАСХОДНИКИ
def socials_raw_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_raw_calculation)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_raw_1)


def socials_raw_calculation(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Расчет безналичным способом':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_2)
    elif user_answer == 'Расчет наличными денежными средствами':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_2)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_raw_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_raw_calculation)


# БЕЗНАЛИЧНЫЙ РАСЧЕТ
def socials_raw_beznal_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_raw_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_2)


def socials_raw_beznal_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_3)


def socials_raw_beznal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_4)


def socials_raw_beznal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_5)


def socials_raw_beznal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_6)


def socials_raw_beznal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_IP_8)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_7)


def socials_raw_beznal_IP_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_beznal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_IP_8)


def socials_raw_beznal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_IP_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_beznal_IP_finish)


def socials_raw_beznal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_8)


def socials_raw_beznal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_9)


def socials_raw_beznal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_10)


def socials_raw_beznal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_11)


def socials_raw_beznal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_beznal_entity_finish)


# НАЛИЧНЫЙ РАСЧЕТ
def socials_raw_nal_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_3)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_raw_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_2)


def socials_raw_nal_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_3)


def socials_raw_nal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_5(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_4)


def socials_raw_nal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_IP_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_IP_6)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_6_1())
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_6_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_5)


def socials_raw_nal_IP_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_nal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_5(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_IP_6)


def socials_raw_nal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_IP_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_IP_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_nal_IP_finish)


def socials_raw_nal_entity_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_5(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_6)


def socials_raw_nal_entity_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_6_1())
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_6_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_7)


def socials_raw_nal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_8)


def socials_raw_nal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_nal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_9)


def socials_raw_nal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_raw_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_raw_nal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_raw_nal_entity_finish)


# На ЗАТРАТЫ ПО ПРИОБРЕТЕНИЮ ОСНОВНЫХ СРЕДСТВ (за исключением легковых автотранспортных средств)
def socials_funds_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_funds_calculation)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_funds_1)


def socials_funds_calculation(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Расчет безналичным способом':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_2)
    elif user_answer == 'Расчет наличными денежными средствами':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_2)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_funds_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_funds_calculation)


# БЕЗНАЛИЧНЫЙ РАСЧЕТ
def socials_funds_beznal_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_funds_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_2)


def socials_funds_beznal_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_3)


def socials_funds_beznal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_4)


def socials_funds_beznal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_5)


def socials_funds_beznal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_6)


def socials_funds_beznal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_7)


def socials_funds_beznal_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_6)


def socials_funds_beznal_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_IP_10)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_9)


def socials_funds_beznal_IP_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_beznal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_IP_10)


def socials_funds_beznal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_IP_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_beznal_IP_finish)


def socials_funds_beznal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_10)


def socials_funds_beznal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_11)


def socials_funds_beznal_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_10)


def socials_funds_beznal_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_13)


def socials_funds_beznal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_beznal_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_beznal_entity_finish)


# НАЛИЧНЫЙ РАСЧЕТ
def socials_funds_nal_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_3)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, 'Выберите способ расчета:',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_funds_calculation)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_2)


def socials_funds_nal_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_3)


def socials_funds_nal_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_4)


def socials_funds_nal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_5)


def socials_funds_nal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_6)


def socials_funds_nal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_IP_8)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_7)


def socials_funds_nal_IP_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_nal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_IP_8)


def socials_funds_nal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_IP_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_nal_IP_finish)


def socials_funds_nal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_8)


def socials_funds_nal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_9)


def socials_funds_nal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_10)


def socials_funds_nal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_nal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_11)


def socials_funds_nal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_funds_nal_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_funds_nal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_funds_nal_entity_finish)


# НА ВЫКУП ПОМЕЩЕНИЯ
def socials_ransom_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_ransom_1)


def socials_ransom_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_ransom_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_2)


def socials_ransom_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_3)


def socials_ransom_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_4)


def socials_ransom_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_6(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_ransom_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_5)


def socials_ransom_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_ransom_7)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_ransom_6)


def socials_ransom_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_IP_8)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_6(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_ransom_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_ransom_7)


def socials_ransom_IP_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_ransom_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_ransom_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_IP_8)


def socials_ransom_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_IP_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_ransom_IP_finish)


def socials_ransom_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_ransom_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_8)


def socials_ransom_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_9)


def socials_ransom_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_10)


def socials_ransom_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_ransom_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_11)


def socials_ransom_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_ransom_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_ransom_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_ransom_entity_finish)


# НА РЕКОНСТРУКЦИЮ ПОМЕЩЕНИЙ
def socials_reconstruction_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_1)


def socials_reconstruction_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_2)


def socials_reconstruction_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_3)


def socials_reconstruction_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_4)


def socials_reconstruction_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_5)


def socials_reconstruction_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_6)


def socials_reconstruction_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_7)


def socials_reconstruction_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_9(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_8)


def socials_reconstruction_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_10(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_10)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_9)


def socials_reconstruction_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_IP_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_IP_11)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_11_1())
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_11_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_9(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_10)


def socials_reconstruction_IP_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_reconstruction_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_10(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_IP_11)


def socials_reconstruction_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_IP_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_IP_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_reconstruction_IP_finish)


def socials_reconstruction_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_10(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_11)


def socials_reconstruction_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_11_1())
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_11_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_12)


def socials_reconstruction_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_14(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_14)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_13)


def socials_reconstruction_entity_14(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_reconstruction_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_14)


def socials_reconstruction_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_reconstruction_entity_14(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_reconstruction_entity_14)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_reconstruction_entity_finish)


# НА КАПИТАЛЬНЫЙ РЕМОНТ
def socials_overhaul_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_1)


def socials_overhaul_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_2)


def socials_overhaul_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_3)


def socials_overhaul_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_4)


def socials_overhaul_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_5)


def socials_overhaul_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_6)


def socials_overhaul_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_7)


def socials_overhaul_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_9)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_8)


def socials_overhaul_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_IP_10)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_9)


def socials_overhaul_IP_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_overhaul_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_IP_10)


def socials_overhaul_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_IP_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_overhaul_IP_finish)


def socials_overhaul_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_10)


def socials_overhaul_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_11)


def socials_overhaul_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_12)


def socials_overhaul_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_overhaul_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_13)


def socials_overhaul_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_overhaul_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_overhaul_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_overhaul_entity_finish)


# НА ОПЛАТУ КОММУНАЛЬНЫХ УСЛУГ
def socials_utilities_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_utilities_1)


def socials_utilities_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_utilities_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_2)


def socials_utilities_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_3)


def socials_utilities_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_4)


def socials_utilities_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_5)


def socials_utilities_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_6)


def socials_utilities_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_utilities_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_7)


def socials_utilities_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_utilities_9)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_utilities_9)


def socials_utilities_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_IP_10)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_utilities_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_utilities_9)


def socials_utilities_IP_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_utilities_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_utilities_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_IP_10)


def socials_utilities_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_IP_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_utilities_IP_finish)


def socials_utilities_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_utilities_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_10)


def socials_utilities_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_11)


def socials_utilities_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_12)


def socials_utilities_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_utilities_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_13)


def socials_utilities_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_utilities_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_utilities_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_utilities_entity_finish)


# НА АРЕНДУ
def socials_rent_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_rent_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_rent_1)


def socials_rent_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_rent_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_2)


def socials_rent_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_3)


def socials_rent_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_4)


def socials_rent_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_5)


def socials_rent_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_6)


def socials_rent_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_rent_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_7)


def socials_rent_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_rent_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_rent_9)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_rent_8)


def socials_rent_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_rent_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_IP_10)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_8(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_rent_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_rent_9)


def socials_rent_IP_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_rent_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_rent_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_IP_10)


def socials_rent_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_IP_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_IP_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_rent_IP_finish)


def socials_rent_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_9(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_rent_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_10)


def socials_rent_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_10_1())
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_10_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_11)


def socials_rent_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_13)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_12)


def socials_rent_entity_13(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_pre_finish(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_rent_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_13)


def socials_rent_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_rent_entity_13(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_rent_entity_13)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_rent_entity_finish)


# НА ПОВЫШЕНИЕ КВАЛИФИКАЦИИ и (или) участие в образовательных программах работников
def socials_high_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_high_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_1)


def socials_high_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_2)


def socials_high_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_4(),
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_high_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_3)


def socials_high_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Расчет безналичным способом':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_5)
    elif user_answer == 'Расчет наличными денежными средствами':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_5(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_high_4)


def socials_high_nal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_6(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_6)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_4(),
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_high_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_5)


def socials_high_nal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_IP_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_IP_7)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_7_1())
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_7_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_5(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_6)


def socials_high_nal_IP_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_10(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_nal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_6(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_IP_7)


def socials_high_nal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_med_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_IP_7(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_IP_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_nal_IP_finish)


def socials_high_nal_entity_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_6(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_7)


def socials_high_nal_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_7_1())
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_7_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_8)


def socials_high_nal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_9)


def socials_high_nal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_11(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_nal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_10)


def socials_high_nal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_nal_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_nal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_nal_entity_finish)


def socials_high_beznal_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_4(),
                         reply_markup=socials.socials_nal_beznal_keyboard())
        bot.register_next_step_handler(message, socials_high_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_5)


def socials_high_beznal_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_6)


def socials_high_beznal_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_8)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_7)


def socials_high_beznal_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_IP_9)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_8)


def socials_high_beznal_IP_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_10(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_beznal_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_IP_9)


def socials_high_beznal_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_med_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_IP_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_beznal_IP_finish)


def socials_high_beznal_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_high_beznal_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_9)


def socials_high_beznal_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_10)


def socials_high_beznal_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_10)


def socials_high_beznal_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_13(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_beznal_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_12)


def socials_high_beznal_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_med_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_high_beznal_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_high_beznal_entity_finish)


# НА МЕД ОБСЛУЖИВАНИЕ ДЕТЕЙ
def socials_med_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_med_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_1)


def socials_med_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_2)


def socials_med_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_3)


def socials_med_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_4)


def socials_med_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_6)


def socials_med_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_7)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_6)


def socials_med_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_med_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_med_8)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_7)


def socials_med_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_IP_9)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_1())
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_7(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_med_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_med_8)


def socials_med_IP_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_10(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_med_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_med_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_IP_9)


def socials_med_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_med_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_IP_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_IP_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_med_IP_finish)


def socials_med_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_8(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_med_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_9)


def socials_med_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_2())
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_9_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_10)


def socials_med_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_12)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_11)


def socials_med_entity_12(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_13(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_med_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_12)


def socials_med_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_med_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_med_entity_12(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_med_entity_12)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_med_entity_finish)


# НА ПРИОБРИТЕНИЕ КОМПЛЕКТУЮЩИХ ИЗДЕЛИЙ
def socials_components_1(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_components_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_2)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, text='На что Вы хотите компенсировать затраты?',
                         reply_markup=socials.socials_kinds_keyboard())
        bot.register_next_step_handler(message, socials_kinds)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_components_1)


def socials_components_2(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_3)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_1(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_components_1)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_2)


def socials_components_3(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_4)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_2)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_3)


def socials_components_4(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_5)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_3(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_3)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_4)


def socials_components_5(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_6(),
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_components_6)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_4(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_4)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_5)


def socials_components_6(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке, что дальше?':
        bot.send_message(message.chat.id, socials_mes.socials_components_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_components_7)
    elif user_answer == 'Чего-то не хватает':
        bot.send_message(message.chat.id, money_mes.money_ramensk_subsidies_IP_no_1(),
                         reply_markup=money.ramensk_subsidies_no_1_link())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=money.back_to_money_ramensk_subsidies())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_5(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_5)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_or_nothing_keyboard())
        bot.register_next_step_handler(message, socials_components_6)


def socials_components_7(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Для индивидуальных предпринимателей':
        bot.send_message(message.chat.id, socials_mes.socials_components_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_IP_8)
    elif user_answer == 'Для юридических лиц':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_8)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_6(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_6)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_components_7)


def socials_components_IP_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_IP_9(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_components_IP_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_components_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_IP_8)


def socials_components_IP_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_components_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_IP_8(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_IP_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_components_IP_finish)


def socials_components_entity_8(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_9)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_7(),
                         reply_markup=socials.socials_IP_or_entity_keyboard())
        bot.register_next_step_handler(message, socials_components_7)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_8)


def socials_components_entity_9(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_10)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_8_1())
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_8_2(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_8)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_9)


def socials_components_entity_10(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_11)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_9(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_9)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_10)


def socials_components_entity_11(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Всё в порядке':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_12(),
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_components_entity_finish)
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_10(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_10)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_11)


def socials_components_entity_finish(message: Message) -> None:
    user_answer = message.text
    if user_answer == 'Как отправить документы':
        bot.send_message(message.chat.id, socials_mes.socials_components_finish(),
                         reply_markup=socials.socials_send_advertisement())
        bot.send_message(message.chat.id, text='На какой этап Вы хотите вернуться ?',
                         reply_markup=socials.socials_finish())
    elif user_answer == '< Назад':
        bot.send_message(message.chat.id, socials_mes.socials_components_entity_11(),
                         reply_markup=socials.socials_all_ok_keyboard())
        bot.register_next_step_handler(message, socials_components_entity_11)
    elif user_answer == '< Вернуться к целям обращения':
        bot.send_message(message.chat.id, choose_service_message(), reply_markup=keyboards.main_aims())
        bot.register_next_step_handler(message, start)
    else:
        bot.send_message(message.chat.id, 'Неправильный ввод. Выберете из списка: ',
                         reply_markup=socials.socials_send_doc())
        bot.register_next_step_handler(message, socials_components_IP_finish)


def start_message(message: Message) -> str:
    if message.chat.first_name is not None:
        return f'Здравствуйте, {message.chat.first_name}👋\n' \
               f'Введите Ваш ИНН\n'
    return f'Здравствуйте 👋\n' \
           f'Введите Ваш ИНН\n'


def phone_message() -> str:
    return f'Введите Ваш номер телефона'


def choose_service_message() -> str:
    return f'Отметьте цель Вашего обращения'


def back_mes() -> str:
    return f'На какой этап Вы хотите вернуться ?'


def error_mes() -> str:
    return f'Я не знаю такой команды...\nВоспользуйтесь клавиатурой снизу'


def wrong() -> str:
    return f'Неправильный ввод.\nВыберете услугу из списка: '


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)
