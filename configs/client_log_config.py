import logging
import os

# выбираем путь до лога клиента и его имя
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'client.log')

# выбор формата записи в обработчик
formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s : %(message)s")

# создание и настройка обработчика
client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
client_handler.setFormatter(formatter)
client_handler.setLevel(logging.INFO)

# создание и настройка регистратора
client_logger = logging.getLogger('client_logger_instance')
client_logger.addHandler(client_handler)
client_logger.setLevel(logging.INFO)
