import logging

def setup_logger(name, level=logging.INFO):
    """Настраивает логгер с выводом в файл и консоль"""
    log_file = "log"

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

    # Добавляем обработчики в логгер 
    logger.addHandler(file_handler)
    #logger.addHandler(console_handler)

    return logger
