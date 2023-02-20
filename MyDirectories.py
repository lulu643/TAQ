class MyDirectories(object):
    Lee = "/Users/lee"
    TempDir = Lee + "/TEMP"
    UnitTests = TempDir + "/UnitTests"

    TAQ = "C:/Users/Lee/Dropbox/Top/Courant/2023/ATQS2023/taq"

    BinRTTradesDir = TAQ + "/trades"
    BinRQQuotesDir = TAQ + "/quotes"


def getTempDir():
    return MyDirectories.TempDir


def getTradesDir():
    return MyDirectories.BinRTTradesDir


def getQuotesDir():
    return MyDirectories.BinRQQuotesDir


def getTAQDir():
    return MyDirectories.TAQ