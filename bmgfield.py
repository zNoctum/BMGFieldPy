from datalogger import Logger
from datasource import Source

def start(source: Source, logger: Logger):
    while True:
        logger.write(source.getData())
