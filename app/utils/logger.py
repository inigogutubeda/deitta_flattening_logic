import logging

def get_logger(name=None):
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(name)
