import select
from logging import getLogger
from socket import socket, AF_INET, SOCK_STREAM
from helpers.message_helper import get_message, send_message

LOGGER = getLogger('server_logger_instance')
ADDRESS = ('', 7777)


class Server:
    def __init__(self):
        """
        Данные сервера
        """
        self.client_sockets = []
        self.client_names = {}
        self.requests = []

    def read_requests(self, ready_to_read):
        """
        Чтение запросов из списка клиентов

        :param ready_to_read: запросы пришедшие на сервер
        """
        for client_socket in ready_to_read:
            try:
                request = get_message(client_socket)
                self.requests.append(request)

                if 'action' in request \
                    and request['action'] == 'presence':
                    self.client_names[request['from']] = client_socket
            except:
                print(f'Клиент {client_socket.getpeername()} отключился')
                LOGGER.info(f'Клиент {client_socket.getpeername()} отключился.')

                self.client_sockets.remove(client_socket)
                client_socket.close()

    def write_responses(self, ready_to_write):
        """
        Сообщение от пишущих - читающим

        :param ready_to_write: запросы гтовые к отправке с сервера
        """

        for client_socket in ready_to_write:
            for request in self.requests:
                if self.client_names[request['to']] == client_socket:
                    try:
                        if 'action' in request \
                                and request['action'] == 'message':
                            send_message(client_socket, request)
                            self.requests.remove(request)
                        elif 'action' in request \
                                and request['action'] == 'presence':
                            request['response'] = 200

                            send_message(client_socket, request)
                            self.requests.remove(request)
                        elif 'action' in request \
                                and request['action'] == 'exit':
                            request['response'] = 200

                            self.client_names.pop(request['from'])

                            send_message(client_socket, request)
                            self.requests.remove(request)
                        else:
                            request['response'] = 400
                            request['error'] = 'Не верный запрос'

                            send_message(client_socket, request)
                            self.requests.remove(request)
                    except:
                        print(f'Клиент {client_socket.getpeername()} отключился')
                        LOGGER.info(f'Клиент {client_socket.getpeername()} отключился.')
                        self.client_sockets.remove(client_socket)
                        client_socket.close()

    def handle(self):
        """
        Основной цикл обработки запросов клиентов
        """
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind(ADDRESS)
        sock.listen(10)
        sock.settimeout(1)

        print('Cервер запущен!')

        while True:
            try:
                client_socket, client_address = sock.accept()
            except OSError:
                pass
            else:
                print(f'Получен запрос на соединение от {client_address}')
                LOGGER.info(f'Получен запрос на соединение от {client_address}')
                self.client_sockets.append(client_socket)

            finally:
                wait = 10
                ready_to_read = []
                ready_to_write = []
                try:
                    ready_to_read, ready_to_write, in_error = select.select(
                        self.client_sockets,
                        self.client_sockets,
                        [],
                        wait
                    )
                except OSError:
                    pass

                self.read_requests(ready_to_read)
                self.write_responses(ready_to_write)


def main():
    server = Server()
    server.handle()


if __name__ == '__main__':
    main()
