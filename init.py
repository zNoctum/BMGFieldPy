import util 

file_prefix = util.getFilePrefix()

import sys
import logging
logging.basicConfig(filename=file_prefix + ".log", encoding="utf-8", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

from datasource import *
from datalogger import *
import bmgfield

logging.info("Started BMGFieldPy")
bmgfield.start(
    Source(FileSource("data.txt"), cycles=150, cycle_length=0.05),
    CSVLogger(file_prefix + ".csv")
)
