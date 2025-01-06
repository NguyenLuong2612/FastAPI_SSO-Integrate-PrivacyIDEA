import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger(name: str, log_file: str = "/var/log/cybersec.log", level: int = logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    log_dir = os.path.dirname(log_file)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.isfile(log_file):
        open(log_file, "a").close()

    file_handler = RotatingFileHandler(log_file, maxBytes=50000000, backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    return logger