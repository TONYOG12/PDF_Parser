import logging

def setup_logger(log_file_path):
    # create logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # create file handler
    fh = logging.FileHandler(log_file_path)
    fh.setLevel(logging.DEBUG)

    # create console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add handlers to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger