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
    def getMGField1(self):
        raise NotImplementedError("Must override getMGField1()!")
    
    @abstractmethod
    def getMGField2(self):
        raise NotImplementedError("Must override getMGField2()!")

    @abstractmethod
    def getTemp(self):
        raise NotImplementedError("Must override getTemp!")
    
    @abstractmethod
    def getRAMUsage(self):
        raise NotImplementedError("Must override getRAMUsage!")

    
    def getTemp(self):
        return 1.0

class FileSource(DataSource):
    def __init__(self, filename: str):
        logging.info("Using Filesource (Sourcefile: %s)", filename)
        with open(filename, "r") as f:
            self.values = [float(line) for line in f.readlines()]
    
    def getMGField1(self):
        return random.choice(self.values)

    def getMGField2(self):
        return random.choice(self.values)

    def getTemp(self):
        return 1.0

    def getRAMUsage(self):
        return 50.0

class SensorSource(DataSource):
    def __init__(self, sensor1_addr=0x48, sensor2_addr=0x49):
        logging.info("Using Sensorsource (sensor1_addr: %02x, sensor2_addr: %02x)", sensor1_addr, sensor2_addr)
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.ads1 = ADS.ADS1115(self.i2c, address=sensor1_addr)
        self.ads1 = ADS.ADS1115(self.i2c, address=sensor2_addr)

    def getMGField1(self):
        x = AnalogIn(self.ads1, ADS.P0)
        y = AnalogIn(self.ads1, ADS.P1)
        z = AnalogIn(self.ads1, ADS.P2)

        return (((x.value * x.value) + (y.value * y.value) + (z.value * z.value)) ** 0.5)
    
    def getMGField1(self):
        x = AnalogIn(self.ads2, ADS.P0)
        y = AnalogIn(self.ads2, ADS.P1)
        z = AnalogIn(self.ads2, ADS.P2)

        return (((x.value * x.value) + (y.value * y.value) + (z.value * z.value)) ** 0.5)
   
    def getTemp(self):
        try:
            with open("/sys/bus/w1/devices/28-01193a114ec3/w1_slave", "r") as sensor:
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
        mgfield1 = 0.0
        mgfield2 = 0.0
        temp = 0.0
        for i in range(self.cycles):
            time.sleep(self.cycle_length)
            mgfield1 += self.source.getMGField1() / self.cycles
            mgfield2 += self.source.getMGField2() / self.cycles
            temp += self.source.getTemp() / self.cycles
            logging.debug('New Reading: %f %f %f', mgfield1, mgfield2, temp)
        out = (self.getDate(), self.getTime(), mgfield1, mgfield2, str("%6.2f" % float(temp)), self.source.getRAMUsage())
        logging.info('New Data Entry: %s', str(out))
        return out
