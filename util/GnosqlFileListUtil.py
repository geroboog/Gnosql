import redis
import time
import pickle

from util.Singleton import Singleton
import copy
from util import Consts

class GnosqlFileListUtil(Singleton):
    memoryDict = {}

    def setMemoryDict(self,dataDict,dataName):
        self.memoryDict[dataName]=copy.deepcopy(dataDict)

    def addMemoryDict(self,dataDict,dataName):
        if self.existMemoryDictData(dataName):
            self.memoryDict[dataName]['data'].append(dataDict)

    def getMemoryDictData(self,dataName):
        if self.existMemoryDictData(dataName):
            return copy.deepcopy(self.memoryDict[dataName])
        else :
            return type(None)

    def getMemoryDictDataReal(self,dataName):
        if self.existMemoryDictData(dataName):
            return self.memoryDict[dataName]
        else :
            return type(None)

    def existMemoryDictData(self,dataName):
        result=False
        if dataName in self.memoryDict.keys():
            result=True
        return result

