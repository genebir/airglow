import logging


def get_logger(name: str):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)d - %(message)s')
    ch.setFormatter(formatter)
    log.addHandler(ch)

    return log
