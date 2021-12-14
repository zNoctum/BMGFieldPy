import util
import logging
import os
from abc import ABC, abstractmethod

class Logger(object):
    @abstractmethod
    def __init__(self, filename: str):
        raise NotImplementedError("Must override __init__(filename)!")

    @abstractmethod
    def write(self, data):
        raise NotImplementedError("Must override write(data)!")

class CSVLogger(Logger):
    file = None
    def __init__(self, filename: str, seperator=",", newline="\n", mgfields=2):
        logging.info("Using CSV Dataformat (seperator=\"%s\", newline=\"%s\")", seperator, util.printSpecialChars(newline))
        logging.info("Output File: %s", filename)
        self.filename = filename
        self.seperator = seperator
        self.newline = newline
        path = os.path.split(filename)[0]
        if not os.path.exists(path):
            os.makedirs(path)
        open(filename, "a+").close()
        if os.path.getsize(filename) == 0:
            mgfields = ["MGField" + str(i + 1) for i in range(mgfields)]
            self.write(["Date", "Time"] + mgfields + ["Temperature", "Ram-Ava, mgfields=2ilable"])

    def write(self, data):
        logging.debug("Wrote %s to %s", str(data), self.filename)
        with open(self.filename, "a+") as f:
            f.write(self.seperator.join([str(item) for item in data]) + self.newline)
