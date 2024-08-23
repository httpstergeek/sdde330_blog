import logging
from typing import Dict


def default_logger(config: Dict):
    logging.basicConfig(
        level=logging.DEBUG,
        filename=f"{config.get('Logpath', './')}/blog.log",
        filemode="a",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger()
    logger.setLevel(config.get("LogLevel", "INFO"))
    return logger
