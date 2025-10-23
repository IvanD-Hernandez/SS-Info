import logging

class CustomFormatter(logging.Formatter):

    RESET = "\x1b[0m"

    DEBUG = "\x1b[38;2;150;222;209m"
    INFO  = "\x1b[38;2;179;255;179m"
    WARN  = "\x1b[38;2;255;255;179m"
    ERROR = "\x1b[38;2;255;179;179m"

    formats = {
        logging.DEBUG:    DEBUG + "%(asctime)s - [DEBUG]  - %(message)s" + RESET,
        logging.INFO:     INFO + "%(asctime)s - [INFO]  - %(message)s" + RESET,
        logging.WARNING:  WARN + "%(asctime)s - [WARN]  - %(message)s" + RESET,
        logging.ERROR:    ERROR + "%(asctime)s - [ERROR] - %(message)s" + RESET,
    }

    def format(self, record):
        log_fmt = self.formats.get(record.levelno, "%(levelname)s - %(message)s")
        original_fmt = self._style._fmt
        self._style._fmt = log_fmt
        
        result = super().format(record)
        self._style._fmt = original_fmt
        return result

def setup_logger(name: str = "bot_logger", level=logging.DEBUG) -> logging.Logger:

    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    if not logger.handlers:
        ch = logging.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(CustomFormatter())
        logger.addHandler(ch)
    
    return logger
