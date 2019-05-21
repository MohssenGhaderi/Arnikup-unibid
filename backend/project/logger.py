
import logging

class Logger:
    __warning_log_addr = "log_warning.txt"
    __error_log_addr = "log_error.txt"
    __info_log_addr = "log_info.txt"
    __debug_log_addr = "log_debug.txt"

    @staticmethod
    def debug(message):
        logging.basicConfig(file_name=Logger.__debug_log_addr, level=logging.DEBUG)
        logging.debug(message)

    @staticmethod
    def info(message):
        logging.basicConfig(file_name=Logger.__info_log_addr, level=logging.INFO)
        logging.info(message)

    @staticmethod
    def warning(message):
        logging.basicConfig(file_name=Logger.__warning_log_addr, level=logging.WARNING)
        logging.warning(message)

    @staticmethod
    def error(message):
        logging.basicConfig(file_name=Logger.__error_log_addr, level=logging.ERROR)
        logging.error(message)
    