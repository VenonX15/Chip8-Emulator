import logging
from chip8.system.config import LOG_LEVEL

def get_logger(name: str = "chip8") -> logging.Logger:
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "[%(levelname)s] %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    logger.setLevel(logging.INFO)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    return logger