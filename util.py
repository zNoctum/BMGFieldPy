from datetime import datetime, date

def getFilePrefix():
    return str(date.today()) + "_" + datetime.now().strftime("%H-%M-%S")

def printSpecialChars(s: str):
    return s.replace("\r", "\\r").replace("\n", "\\n").replace("\t", "\\t")
