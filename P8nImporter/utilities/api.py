import time
from functools import wraps

from ..config.logging import logger

# Define the maximum number of retries and the delay between retries
MAX_RETRIES = 3
RETRY_DELAY = 1  # in seconds

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 0
        while retries < MAX_RETRIES:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.warning(f"Failed to execute {func.__name__}: {e}. Retrying...")
                retries += 1
                time.sleep(RETRY_DELAY)
        raise Exception(f"Failed to execute {func.__name__} after {MAX_RETRIES} retries.")

    return wrapper

