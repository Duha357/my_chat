import logging
import os
import sys

# выбираем путь до лога клиента и его имя
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, '../logs/client.log')

# выбор формата записи в обработчик
formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s : %(message)s")

# создание и настройка потока
stream = logging.StreamHandler(sys.stderr)
stream.setFormatter(formatter)
stream.setLevel(logging.INFO)

# создание и настройка обработчика
client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
client_handler.setFormatter(formatter)

# создание и настройка регистратора
client_logger = logging.getLogger('client_logger_instance')
client_logger.addHandler(stream)
client_logger.addHandler(client_handler)
client_logger.setLevel(logging.INFO)
