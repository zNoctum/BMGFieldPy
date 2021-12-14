import util 

file_prefix = util.getFilePrefix()

import sys
import logging
logging.basicConfig(filename="log/" + file_prefix + ".log", encoding="utf-8", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

from datasource import *
from datalogger import *
import bmgfield

logging.info("Started BMGFieldPy")
bmgfield.start(
    Source(FileSource("data.txt"), cycles=1, cycle_length=0.5),
    CSVLogger("csv/" + file_prefix + ".csv")
)
