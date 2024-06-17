# logging_config.py
import logging

from config.settings import DEBUG


def configure_logging():
    logging.basicConfig(
        level=logging.DEBUG if DEBUG else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],  # Ensure logs are sent to stdout
    )

    logger = logging.getLogger(__name__)
    return logger
