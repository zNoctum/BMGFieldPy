from abc import ABC, abstractmethod
from datetime import datetime, date
import logging
import time
import random
import psutil
try:
    from adafruit_ads1x15.analog_in import AnalogIn
    import adafruit_ads1x15.ads1115 as ADS
    import busio
    import board
except:
    pass

class DataSource(object):
    @abstractmethod
    def getMGField(self, i: int):
        raise NotImplementedError("Must override getMGField1()!")
    
    @abstractmethod
    def getTemp(self):
        raise NotImplementedError("Must override getTemp!")
    
    @abstractmethod
    def getRAMUsage(self):
        raise NotImplementedError("Must override getRAMUsage!")

    
    def getTemp(self):
        return 1.0

class FileSource(DataSource):
    mgfields = 0
    def __init__(self, filename: str):
        logging.info("Using Filesource (Sourcefile: %s)", filename)
        self.mgfields = 2
        with open(filename, "r") as f:
            self.values = [float(line) for line in f.readlines()]
    
    def getMGField(self, i: int):
        return random.choice(self.values)

    def getTemp(self):
        return 1.0

    def getRAMUsage(self):
        return 50.0

class SensorSource(DataSource):
    ads = []

    def __init__(self, temp_id: str, addrs=[0x48]):
        logging.info("Using Sensorsource (addrs: %s)", str(addrs))
        self.temp_id = temp_id
        self.i2c = busio.I2C(board.SCL, board.SDA)
        for addr in addrs:
            self.ads.append(ADS.ADS1115(self.i2c, address=addr))
        self.mgfields = len(self.ads)

    def getMGField(self, i: int):
        x = AnalogIn(self.ads[i], ADS.P0)
        y = AnalogIn(self.ads[i], ADS.P1)
        z = AnalogIn(self.ads[i], ADS.P2)

        return (((x.value * x.value) + (y.value * y.value) + (z.value * z.value)) ** 0.5)
    
    def getTemp(self):
        try:
            with open("/sys/bus/w1/devices/" + self.temp_id + "/w1_slave", "r") as sensor:
                temp_string = sensor.read().split("\n")[1].split(" ")[9]
                temp = float(temp_string[2:]) / 1000
        except Exception as exception:
            temp = 1.00
            logging.warn('Failed to read Temp', exc_info=True)
        return temp

    def getRAMUsage(self):
        return float(psutil.virtual_memory().available * 100 / psutil.virtual_memory().total)

class Source(object):
    def __init__(self, source: DataSource, cycles, cycle_length):
        self.cycles = cycles
        self.cycle_length = cycle_length
        self.source = source

    def getDate(self):
        return date.today().strftime("%Y-%m-%d")

    def getTime(self):
        return datetime.today().strftime("%H-%M-%S")

    def getData(self):
        mgfields = [0] * self.source.mgfields
        temp = 0.0
        for i in range(self.cycles):
            time.sleep(self.cycle_length)
            for i in range(self.source.mgfields):
                mgfields[i] += self.source.getMGField(i) / self.cycles
            temp += self.source.getTemp() / self.cycles
            logging.debug('New Reading: %f %f %f', mgfields, temp)
        out = [self.getDate(), self.getTime(), ] + mgfields + [ str("%6.2f" % float(temp)), self.source.getRAMUsage()]
        logging.info('New Data Entry: %s', str(out))
        return out
