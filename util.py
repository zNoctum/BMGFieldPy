from datetime import datetime, date

def getFilePrefix():
    return date.today()) + "_" + str(datetime.now().strftime("%H-%M-%S")
