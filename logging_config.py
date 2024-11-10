# logging_config.py

import logging

def configure_logging():
    """
    Configures the logging settings for the application.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
