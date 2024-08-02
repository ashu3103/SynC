import logging
from constants import *

def configureLogger(format, level=logging.DEBUG, fileHandler=None, streamHandler=None):
    if (not fileHandler):
        fileHandler = f'{APP_PATH}/app.log'
    logging.basicConfig(
        level=level,
        format=format,
        handlers=[
            logging.FileHandler((fileHandler)),
            logging.StreamHandler(streamHandler)
        ]
    )

def initiateLogging(name, logFile=None):
    if (not logFile):
        logFile = f'{APP_PATH}/app.log'
    open(logFile, 'w').close()

    logger = logging.getLogger(name)
    return logger