import logging
from datetime import date


def get_today():
    today = date.today()
    dt_string = today.strftime("%d_%m_%Y")
    return dt_string


def logerror(error):
    logging.basicConfig(level=logging.DEBUG)
    logging.info(error)
