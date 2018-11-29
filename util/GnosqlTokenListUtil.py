import redis
import time
import pickle

from util.Singleton import Singleton
from util.ClockUtil import ClockUtil
import copy

class GnosqlTokenListUtil(Singleton):
    tokenDict = {}
    loginDict = {}

    def setTokenDict(self,dataDict,token):
        self.tokenDict[token]=copy.deepcopy(dataDict)

    def setLoginDict(self,dataDict,username):
        self.loginDict[username]=copy.deepcopy(dataDict)

    def getTokenDictData(self,token):
        if self.existTokenDictData(token):
            return copy.deepcopy(self.tokenDict[token])
        else :
            return type(None)

    def existTokenDictData(self,token):
        result=False
        if token in self.tokenDict.keys():
            result=True
        return result

    def existToken(self,token,username):
        result=False
        if token in self.tokenDict.keys():
            thisUsername=self.tokenDict[token]['username']
            if thisUsername==username :
                result=True
        return result

    def existLogin(self,username):
        result=False
        if username in self.loginDict.keys():
                result=True
        return result

    def getToken(self,username):
        token=self.getTokenDictData(username)
        ##转化token
        times =  ClockUtil.getTimes()
        times=times+self.loginDict[username]["guid"]
        token = times
        result={"token":token,"username":username}
        self.setTokenDict(result,token)

        return token

    def generateGnosqlId(self,username):
        times =  ClockUtil.getTimes();
        gnosql=self.loginDict[username]["guid"]+times;
        return gnosql;
