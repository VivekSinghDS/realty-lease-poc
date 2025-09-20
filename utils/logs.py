import logging
import logging.config


# The `LoggingManager` class initializes a logging system with a specified log # level and provides a method to retrieve loggers by name.
class LoggingManager:
    def __init__(self, log_level=logging.DEBUG):
        self.log_level = log_level
        self._setup_logging()

    def _setup_logging(self):
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"message_only": {"format": "%(message)s"}},
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": self.log_level,
                    "formatter": "message_only",
                    "stream": "ext://sys.stdout",
                }
            },
            "root": {
                "handlers": ["console"],
                "level": self.log_level,
                "propagate": True,
            },
        }
        logging.config.dictConfig(log_config)

    def get_logger(self, name):
        return logging.getLogger(name)


log_manager = LoggingManager(log_level=logging.INFO)
logging.getLogger("kafka").setLevel(logging.CRITICAL)
logger = log_manager.get_logger(__name__)

if __name__ == "__main__":
    log_manager = LoggingManager(log_level=logging.INFO)
    logger = log_manager.get_logger(__name__)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
