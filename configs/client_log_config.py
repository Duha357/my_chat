import logging
import os

# абсолютный путь
LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
# путь к клиент логу
CLIENT_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'client_log.log')

client_logger = logging.getLogger('client_logger_instance')
client_logger.setLevel(logging.INFO)

client_handler = logging.FileHandler(CLIENT_LOG_FILE_PATH, encoding='utf-8')
client_handler.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s , %(levelname)s : %(module)s - %(message)s")
client_handler.setFormatter(formatter)

# добавляю один обработчик
client_logger.addHandler(client_handler)

