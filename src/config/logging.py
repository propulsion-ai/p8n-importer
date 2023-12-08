# config/logger_config.py
import logging

def setup_logger(level=logging.WARNING):
    """
    Set up a logger with the specified logging level.

    Args:
        level (int): The logging level to set for the logger. Defaults to logging.WARNING.

    Returns:
        logging.Logger: The configured logger instance.
    """
    logger = logging.getLogger("p8n-importer")
    logger.setLevel(level)

    # Create console handler
    c_handler = logging.StreamHandler()
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)

    if not logger.hasHandlers():
        logger.addHandler(c_handler)

    return logger

# Configure the logger with default level
logger = setup_logger()
