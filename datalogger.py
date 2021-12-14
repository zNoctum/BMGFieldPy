import util
import logging
import os
from abc import ABC, abstractmethod

HEADER = ["Date", "Time", "MGField Value1","MGField Value2", "Temperature", "Ram-Available"]

class Logger(object):
    @abstractmethod
    def __init__(self, filename: str):
        raise NotImplementedError("Must override __init__(filename)!")

    @abstractmethod
    def write(self, data):
        raise NotImplementedError("Must override write(data)!")

class CSVLogger(Logger):
    file = None
    def __init__(self, filename: str, seperator=",", newline="\n", header=HEADER):
        logging.info("Using CSV Dataformat (seperator=\"%s\", newline=\"%s\")", seperator, util.printSpecialChars(newline))
        logging.info("Output File: %s", filename)
        self.seperator = seperator
        self.newline = newline
        self.file = open(filename, 'a+')
        if os.path.getsize(filename) == 0:
            self.write(header)

    def write(self, data):
        self.file.write(self.seperator.join([str(item) for item in data]) + self.newline)

    def __del__(self):
        self.file.close()
