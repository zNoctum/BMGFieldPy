from datasource import *
from datalogger import *
import bmgfield

bmgfield.start(
    Source(FileSource("data.txt"), cycles=150, cycle_length=0),
    CSVLogger("out.csv")
)
