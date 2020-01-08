import logging.handlers
import os

# выбираем путь до лога сервера и его имя
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
SERVER_LOF_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'server.log')

# выбор формата записи в обработчик
formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s : %(message)s")

# создание и настройка обработчика
server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOF_FILE_PATH, encoding='utf8', when='d')
server_handler.setFormatter(formatter)
server_handler.setLevel(logging.INFO)

# создание и настройка регистратора
server_logger = logging.getLogger('server_logger_instance')
server_logger.addHandler(server_handler)
server_logger.setLevel(logging.INFO)
