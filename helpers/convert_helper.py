import json
from configs.config import ENCODING


def dict_to_bytes(message_dict):
    """
    Преобразование словаря в байты

    :param message_dict:
    :return:
    """
    if isinstance(message_dict, dict):
        jmessage = json.dumps(message_dict)
        bmessage = jmessage.encode(ENCODING)

        return bmessage
    else:
        raise TypeError


def bytes_to_dict(message_bytes):
    """
    Получение словаря из байтов

    :param message_bytes:
    :return:
    """
    if isinstance(message_bytes, bytes):
        jmessage = message_bytes.decode(ENCODING)
        try:
            message = json.loads(jmessage)
        except:
            message = jmessage

        if isinstance(message, dict):
            return message
        else:
            raise TypeError
    else:
        raise TypeError


def send_message(sock, message):
    """
    Отправка сообщения

    :param sock:
    :param message:
    """
    try:
        bprescence = dict_to_bytes(message)
    except TypeError:
        bprescence = message.encode(ENCODING)

    sock.send(bprescence)


def get_message(sock):
    """
    Получение сообщения

    :param sock: сокет
    :return: словарь ответа
    """
    bresponse = sock.recv(4096)
    try:
        response = bytes_to_dict(bresponse)
    except TypeError:
        response = bresponse.decode(ENCODING)

    return response
