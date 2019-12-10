import sys
import time
import random
import threading
import log.client_log_config
from logging import getLogger
from log.decorators import log
from socket import socket, AF_INET, SOCK_STREAM
from jim.config import *
from jim.utils import get_message, send_message


logger = getLogger('client_logger_instance')
ADDRESS = ('localhost', 7777)


@log(logger)
def create_presence(account_name):
    """
    Формирование ​​сообщения о присутствии
    :param account_name: имя пользователя
    :return: словарь сообщения
    """
    if not isinstance(account_name, str):
        raise TypeError

    message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }

    return message


@log(logger)
def create_message(account_name, destination, text):
    """
    Формирование ​​сообщения о присутствии
    :param account_name: имя пользователя
    :param destination: получатель
    :param text: передаваемый текст
    :return: словарь сообщения
    """
    if not isinstance(account_name, str):
        raise TypeError

    message = {
        ACTION: MSG,
        TIME: time.time(),
        TO: destination,
        FROM: account_name,
        MSG: text
    }

    return message


@log(logger)
def translate_message(message):
    """
    Разбор сообщения
    :param message: словарь ответа от сервера
    :return: корректный словарь ответа
    """
    if not isinstance(message, dict):
        raise TypeError

    code = message[RESPONSE]

    return f'Код подключения: {code}'


def read_messages(client, account_name):
    """
    Постоянное получение сообщений клиентом
    :param client: сокет клиента
    """
    while True:
        message = get_message(client)
        if message['from'] != account_name:
            print(message['message'])


def client_unit():
    """
    Создание клиента
    """
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(ADDRESS)

        account_name = f'{random.choice(NAME)}'
        send_message(sock, create_presence(account_name))
        server_response = get_message(sock)
        translate_response = translate_message(server_response)
        print(translate_response)
        print(f'Ваше имя: {account_name}')

        if translate_response == 'Код подключения: 200':
            t = threading.Thread(target=read_messages, args=(sock, account_name))
            t.start()

            while True:
                msg = input('> ')
                if msg.startswith('message'):
                    params = msg.split()
                    try:
                        to = params[1]
                        text = f' '.join(params[2:])
                    except IndexError:
                        print('Не задан получатель или текст сообщения')
                    else:
                        message = create_message(account_name, to, text)
                        send_message(sock, message)
                elif msg == 'help':
                    print('message <получатель> <текст> - отправить сообщение')
                elif msg == 'exit':
                    break
                else:
                    print('Неверная команда, для справки введите help')

            sock.disconnect()


if __name__ == '__main__':
    client_unit()