import logging.handlers
import os

# абсолютный путь
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь к сервер логу
SERVER_LOF_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'server_log.log')

server_logger = logging.getLogger('server_logger_instance')
server_logger.setLevel(logging.INFO)

# ротация файлов по дням
server_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOF_FILE_PATH, when='d')  # d - значит, ротация по дням

formatter = logging.Formatter("%(asctime)s , %(levelname)s : %(module)s - %(message)s")
server_handler.setFormatter(formatter)

# добавляю один обработчик
server_logger.addHandler(server_handler)
