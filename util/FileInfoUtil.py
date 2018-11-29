import time
import datetime

import os

from numpy import unicode


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def getFileSize(filePath):
    fsize = os.path.getsize(filePath)
    return str(fsize)+"KB"


def getFileAccessTime(filePath):
    t = os.path.getatime(filePath)
    return TimeStampToTime(t)


def getFileCreateTime(filePath):
    t = os.path.getctime(filePath)
    return TimeStampToTime(t)


def getFileModifyTime(filePath):
    t = os.path.getmtime(filePath)
    return TimeStampToTime(t)
