import logging
from os import path, remove

# TODO: add modules from this package (?)
from .mail import MailServer

# http://www.patricksoftwareblog.com/python-logging-tutorial/

# If applicable, delete the existing log file to generate a fresh log file
# during each execution
if path.isfile("22-06-18-generate-evaluation-surveys.log"):
    remove("22-06-18-generate-evaluation-surveys.log")

# Create the Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create the Handler for logging data to a file
logger_handler = logging.FileHandler('22-06-18-generate-evaluation-surveys.log')
logger_handler.setLevel(logging.DEBUG)

# Create a Formatter for formatting the log messages
logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')

# Add the Formatter to the Handler
logger_handler.setFormatter(logger_formatter)

# Add the Handler to the Logger
logger.addHandler(logger_handler)
logger.info('Completed configuring logger()!')

