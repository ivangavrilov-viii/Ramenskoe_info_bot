from telebot.types import Chat


class BotUser:
    """ Класс: Пользователь Телеграм-бота. """

    def __init__(self, chat: Chat) -> None:
        self.first_name = chat.first_name
        self.last_name = chat.last_name
        self.inn: int() = None
        self.phone = str()
        self.username = chat.username
        self.start_time = None
        self.end_time = None
        self.bot_way = str()
        self.user_id = chat.id

    def __str__(self) -> str:
        return f'First name: {self.first_name}, Last name: {self.last_name}, User ID: {self.user_id}, ' \
               f'User INN: {self.inn}, User PHONE: {self.phone}, Username: @{self.username}, ' \
               f'Start time: {self.start_time}, End time: {self.end_time}, User way: {self.bot_way}'

    def insert_in_table(self) -> list:
        first_name = f'{self.first_name}'
        last_name = f'{self.last_name}'
        inn = f'{self.inn}'
        phone = f'{self.phone}'
        username = f'@{self.username}'
        start_time = f'{self.start_time}'
        end_time = f'{self.end_time}'
        bot_way = f'{self.bot_way}'
        user_id = f'{self.user_id}'

        return [user_id, phone, inn, first_name, last_name, username, start_time, end_time, bot_way]
