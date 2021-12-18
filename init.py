import util 

file_prefix = util.getFilePrefix()

import sys
import logging
logging.basicConfig(filename="log/" + file_prefix + ".log", level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

from datasource import *
from datalogger import *
import bmgfield

logging.info("Started BMGFieldPy")
bmgfield.start(
    Source(SensorSource("28-01204b515089", addrs=[0x48]), cycles=150, cycle_length=0.5),
    CSVLogger("csv/" + file_prefix + ".csv")
)
