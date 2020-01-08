import logging.handlers
import os
import sys

# выбираем путь до лога сервера и его имя
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
SERVER_LOF_FILE_PATH = os.path.join(LOG_FOLDER_PATH, '../logs/server.log')

# выбор формата записи в обработчик
formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s : %(message)s")

# создание и настройка потока
stream = logging.StreamHandler(sys.stderr)
stream.setFormatter(formatter)
stream.setLevel(logging.INFO)

# создание и настройка обработчика
server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOF_FILE_PATH, encoding='utf8', when='d')
server_handler.setFormatter(formatter)

# создание и настройка регистратора
server_logger = logging.getLogger('server_logger_instance')
server_logger.addHandler(stream)
server_logger.addHandler(server_handler)
server_logger.setLevel(logging.INFO)
