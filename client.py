import json
import time
import random
import threading
import logging
import configs.client_log_config
from socket import socket, AF_INET, SOCK_STREAM
from configs.client_name_config import *
from decorators.log_decorator import log
from helpers.message_helper import get_message, send_message

LOGGER = logging.getLogger('client_logger_instance')
ADDRESS = ('127.0.0.1', 7777)


class ClientSender(threading.Thread):
    def __init__(self, account_name, sock):
        """
        Данные клиента

        :param account_name: имя пользователя
        :param sock: сокет пользователя
        """
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    @log(LOGGER)
    def presence_request(self):
        """
        Формирование ​​сообщения о присутствии

        :return: словарь сообщения
        """
        return {
            'action': 'presence',
            'time': time.time(),
            'to': self.account_name,
            'from': self.account_name,
        }

    @log(LOGGER)
    def exit_request(self):
        """
        Формирование ​​сообщения о выходе

        :return: словарь сообщения
        """
        return {
            'action': 'exit',
            'time': time.time(),
            'to': self.account_name,
            'from': self.account_name,
        }

    @log(LOGGER)
    def create_message(self, to_account, text):
        """
        Формирование ​​сообщения для передачи

        :param to_account: имя пользователя
        :param text: передаваемый текст
        :return: словарь сообщения
        """
        if not isinstance(to_account, str):
            raise TypeError

        return {
            'action': 'message',
            'time': time.time(),
            'to': to_account,
            'from': self.account_name,
            'message': text
        }

    def run(self):
        """
        Ввод команд клиентом
        """
        send_message(self.sock, self.presence_request())

        # ждём пока придёт ответ сервера о присутствии
        time.sleep(3)
        print('help - для справки')

        while True:
            command = input('Введите команду:\n')

            params = command.split()

            if params[0] == 'message':
                try:
                    to = params[1]
                    text = f' '.join(params[2:])
                except IndexError:
                    print('Не задан получатель или текст сообщения')
                else:
                    send_message(self.sock, self.create_message(to, text))
            elif params[0] == 'help':
                print('message <получатель> <текст> - отправить сообщение')
            elif params[0] == 'exit':
                send_message(self.sock, self.exit_request())

                print('Соединение с сервером завершено!')
                LOGGER.info('Завершено соединение с сервером')

                break
            else:
                print('Неверная команда, для справки введите help')


class ClientReader(threading.Thread):
    def __init__(self, account_name, sock):
        """
        Данные клиента

        :param account_name: имя пользователя
        :param sock: сокет пользователя
        """
        self.account_name = account_name
        self.sock = sock
        super().__init__()

    @log(LOGGER)
    def presence_response(self, message):
        """
        Разбор ответа сервера о присутствии

        :param message: словарь ответа от сервера
        :return: статус подключения
        """
        if not isinstance(message, dict):
            raise TypeError

        print(message)

        if message['response'] == 200:
            print(f'Cоединение с сервером установлено')
            LOGGER.info(f'Cоединение с сервером установлено')
        elif message['response'] == 400:
            print(f"Код подключения: 400 : {message['error']}")
            LOGGER.info(f"Код подключения: 400 : {message['error']}")

    def run(self):
        """
        Постоянное получение сообщений клиентом
        """
        while True:
            try:
                message = get_message(self.sock)

                if 'action' in message \
                    and message['action'] == 'message' \
                        and message['to'] == self.account_name:
                    print(f"\nСообщение от пользователя {message['from']}: {message['message']}")
                    print(f"Введите команду:")
                elif 'action' in message \
                    and message['action'] == 'presence' \
                        and message['to'] == self.account_name:
                    self.presence_response(message)
            except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError, json.JSONDecodeError):
                LOGGER.critical('Потеряно соединение с сервером')
                break


def main():
    client_name = f'{random.choice(NAME)}'

    print(f'Клиент {client_name} запущен')
    LOGGER.info(f'Клиент {client_name} запущен')

    print('Подождите пока установится соединение с сервером...')

    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect(ADDRESS)
    except json.JSONDecodeError:
        LOGGER.error('Не удалось декодировать полученную Json строку.')
        exit(1)
    except (ConnectionRefusedError, ConnectionError):
        LOGGER.critical(f'Не удалось подключиться к серверу {ADDRESS}')
        exit(1)
    else:
        reader = ClientReader(client_name, sock)
        reader.daemon = True
        reader.start()

        sender = ClientSender(client_name, sock)
        sender.daemon = True
        sender.start()

        while True:
            time.sleep(5)
            if reader.is_alive() and sender.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
