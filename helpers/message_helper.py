import json


def dict_to_bytes(message_dict):
    """
    Преобразование словаря в байты

    :param message_dict: словарь сообщения
    :return: сообщение из байтов
    """
    if not isinstance(message_dict, dict):
        raise TypeError

    json_message = json.dumps(message_dict)

    return json_message.encode('utf-8')


def bytes_to_dict(message_bytes):
    """
    Получение словаря из байтов

    :param message_bytes: сообщение из байтов
    :return: словарь сообщения
    """
    if not isinstance(message_bytes, bytes):
        raise TypeError

    json_message = message_bytes.decode('utf-8')

    return json.loads(json_message)


def send_message(sock, message_dict):
    """
    Отправка сообщения

    :param sock: используемый сокет
    :param message_dict: словарь отправки сообщения
    """
    message_bytes = dict_to_bytes(message_dict)

    sock.send(message_bytes)


def get_message(sock):
    """
    Получение сообщения

    :param sock: используемый сокет
    :return: словарь получения сообщения
    """
    message_bytes = sock.recv(4096)

    return bytes_to_dict(message_bytes)
