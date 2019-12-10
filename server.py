import select
import log.server_log_config
from logging import getLogger
from log.decorators import log
from socket import socket, AF_INET, SOCK_STREAM
from jim.utils import get_message, send_message
from jim.config import *


logger = getLogger('server_logger_instance')
ADDRESS = ('', 7777)


@log(logger)
def presence_response(presence_message):
    """
    Формирование ответа клиенту
    :param presence_message: Словарь presence запроса
    :return: Словарь ответа
    """
    if ACTION in presence_message and \
            presence_message[ACTION] == PRESENCE and \
            TIME in presence_message and \
            isinstance(presence_message[TIME], float):

        return {RESPONSE: 200}
    else:
        return {RESPONSE: 400, ERROR: 'Не верный запрос'}


def read_requests(r_clients, all_clients):
    '''
    Чтение запросов из списка клиентов
    '''
    responses = {}

    for sock in r_clients:
        try:
            data = sock.recv(4096).decode('utf-8')
            responses[sock] = data
        except:
            print(f'Клиент {sock.getpeername()} отключился')
            all_clients.remove(sock)

    return responses


def write_responses(requests, w_clients, all_clients):
    '''
    Сообщение от пишущих - читающим
    '''

    for sock in w_clients:
        for i in requests:
            try:
                resp = requests[i].encode('utf-8')
                sock.send(resp)
            except:
                print(f'Клиент {sock.getpeername()} отключился')
                sock.close()
                all_clients.remove(sock)


def mainloop():
    '''
    Основной цикл обработки запросов клиентов
    '''
    clients = []

    server = socket(AF_INET, SOCK_STREAM)
    server.bind(ADDRESS)
    server.listen(5)
    server.settimeout(1)

    while True:
        try:
            client, addr = server.accept()
        except OSError:
            pass
        else:
            print(f'Получен запрос на соединение от {str(addr)}')
            clients.append(client)

            presence = get_message(client)
            print(presence)
            server_response = presence_response(presence)
            send_message(client, server_response)
        finally:
            wait = 10
            r = []
            w = []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except:
                pass

            requests = read_requests(r, clients)
            if requests:
                write_responses(requests, w, clients)


if __name__ == '__main__':
    print('Cервер запущен!')
    mainloop()