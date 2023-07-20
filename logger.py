import logging


def setup_logger(log_file, level=logging.INFO):
    logger = logging.getLogger("my_logger")
    logger.setLevel(level)
    file_handler = logging.FileHandler(log_file)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger


log_file = "errors.log"
log = setup_logger(log_file)
