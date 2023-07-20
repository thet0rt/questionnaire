import logging


def setup_logger(log_file, level=logging.INFO):
    # Create a logger
    logger = logging.getLogger("my_logger")
    logger.setLevel(level)

    # Create a file handler
    file_handler = logging.FileHandler(log_file)

    # Create a formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger


log_file = "errors.log"
log = setup_logger(log_file)
