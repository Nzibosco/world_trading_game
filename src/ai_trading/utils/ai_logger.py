import logging
import datetime

def app_logger(base_file_name):
    # Generate the current timestamp and format it
    current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    # Concatenate the base file name with the current timestamp
    full_file_name = f"{base_file_name}_{current_time}.log"

    # Create a logger
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)  # This will log all levels (DEBUG and above)

    # Create a handler for writing log messages to a file
    file_handler = logging.FileHandler(full_file_name)
    file_handler.setLevel(logging.DEBUG)  # Set the log level for this handler

    # Create a handler for writing log messages to the console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Set the log level for this handler

    # Create a formatter to specify the format of the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


