import logging
from project1.database.models import log_entry
from project1.database.database import get_db

def setup_logger(name, level=logging.INFO):
    """Настраивает логгер с выводом в файл и консоль"""
    log_file = "log.txt"

    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Формат сообщений
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Обработчик для файла
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    
    # Обработчик для консоли
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Обработчик для базы данных
    db = next(get_db())

    class DBHandler(logging.Handler):
        def emit(self,record):
            __log = log_entry(level=record.levelname, message=record.getMessage())
            db.add(__log)
            db.commit()

    db_handler = DBHandler()

    # Добавляем обработчики в логгер 
    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)
    logger.addHandler(db_handler)

    return logger
