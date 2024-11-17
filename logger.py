import logging

logger = logging.getLogger()


ch = logging.StreamHandler()

formatter = logging.Formatter(
    '%(message)s'
)

ch.setFormatter(formatter)

logger.addHandler(ch)
logger.setLevel(logging.INFO)
