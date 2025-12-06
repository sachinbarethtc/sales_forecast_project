# import logging
# import os

# LOG_DIR = "logs"
# os.makedirs(LOG_DIR, exist_ok=True)

# LOG_FILE = os.path.join(LOG_DIR, "app.log")

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler(LOG_FILE, mode="a", encoding="utf-8")
#     ]
# )

# logger = logging.getLogger("forecast-app")


# app/logger.py
import logging
import sys

LOG_FORMAT = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
DATEFMT = "%Y-%m-%d %H:%M:%S"

def get_logger(name="forecast-app", level=logging.INFO):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt=DATEFMT))
    logger.addHandler(handler)
    # reduce verbosity from libraries if desired
    logging.getLogger("sqlalchemy").setLevel(logging.WARNING)
    return logger

logger = get_logger()
