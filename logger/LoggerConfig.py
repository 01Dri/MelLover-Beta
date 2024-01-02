import logging


class LoggerConfig:
    def __init__(self):
        logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(name)s: %(message)s')
        self.logger = logging.getLogger("MEL LOVER")

    def config_logger_level(self, level):
        self.logger.setLevel(level)
        return self

    def get_logger(self):
        return self.logger

    def get_logger_info_level(self):
        self.logger.setLevel(logging.INFO)
        return self.logger

    def get_logger_info_error(self):
        self.logger.setLevel(logging.ERROR)
        return self.logger
