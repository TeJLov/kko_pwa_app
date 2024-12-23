import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# В начале файла:
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))  # Переход на два уровня вверх к корню проекта
log_directory = os.path.join(PROJECT_ROOT, "logs")

if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Настраиваем форматирование
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Создаем файл лога с датой
current_date = datetime.now().strftime('%Y-%m-%d')
file_handler = RotatingFileHandler(
    os.path.join(log_directory, f'kko_site_{current_date}.log'),
    maxBytes=10485760,  # 10MB
    backupCount=5
)
file_handler.setFormatter(formatter)

# Настраиваем вывод в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Создаем логгер
logger = logging.getLogger('kko_site')
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Функция для логирования ошибок с дополнительной информацией
def log_error(error: Exception, additional_info: str = None):
    error_message = f"Error: {str(error)}"
    if additional_info:
        error_message += f" | Additional Info: {additional_info}"
    logger.error(error_message)
