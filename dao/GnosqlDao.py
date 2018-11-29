from dao import BaseDao
from util import MysqlUtil
from util import MapUtil
from util import Consts
import json
import codecs
import os
from util.ClockUtil import ClockUtil
from util.GnosqlFileListUtil import GnosqlFileListUtil
import time
from util.MatchUtil import MatchUtil


def foreach(function, iterator):
    for item in iterator:
        function(item)


class GnosqlDao(BaseDao.BaseDao):#user@[{\"@userId\":3}]
    # 定义构造方法
    def __init__(self):
        # self.mysqlUtil = MysqlUtil.MysqlUtil()
        pass

    def get_selectedArray(self,data):
        dataArr=data.split(Consts.thisSeparaterArr)
        tableName=dataArr[0]
        fileName=self.getFileName(tableName)
        fileState=os.path.exists(fileName)
        if fileState:
            GF=GnosqlFileListUtil();
            #这里是从内存里面获取到数据字典
            dataDict=GF.getMemoryDictData(tableName)
            data="["+dataArr[1]
            #这里把数据字典内的数据取出
            if dataDict!=type(None):
                dataArr=dataDict["data"]
            else:
                myNosqlfile = codecs.open(fileName, "r")
                text = myNosqlfile.read()
                myNosqlfile.close()
                dataArr=[]
                if text!="" :
                    dataArr=json.loads(text)
                dataDict= {"data": dataArr}
                GF.setMemoryDict(dataDict,tableName)
            #首先获取到当前数据表所有数据
            resultArr=[]
            #获取需要查询的数据
            selectArr=json.loads(data)
            selectAndArr=[]
            selectAndSize=0
            selectOrSize=0
            selectOrArr=[]
            #json格式扩展
            for key,selectValue in enumerate(selectArr):
                for singleKey,singleValue in selectValue.items():
                    if singleKey.find(Consts.andSeparater) > -1:
                        selectAndArr.append({singleKey:singleValue});
                        selectAndSize += 1
                    elif  singleKey.find(Consts.orSeparater) > -1:
                        selectOrArr.append({singleKey:singleValue});
                        selectOrSize += 1;

            print(json.dumps(selectAndArr))
            print(json.dumps(selectOrArr))

            selectSize=len(selectArr);
            resultSize=0;
            singleCheck=0;
            #先查询出所有的与结果
            if selectAndSize>0:
                for dataKey,dataValue in enumerate(dataArr):
                    checkSize=0;
                    #对每个数据进行匹配
                    #每个条件进行匹配
                    for key,selectValue in enumerate(selectAndArr):
                        singleCheck=0;
                        for singleKey,singleValue in selectValue.items():
                            thisKey=singleKey.strip('@');
                            if thisKey in dataValue.keys():
                                if not MatchUtil.match(singleValue, dataValue[thisKey]):
                                    singleCheck+=1;
                                else:
                                    checkSize+=1;
                        if singleCheck!=0:
                            break;

                    if checkSize==selectAndSize and checkSize!=0 and selectAndSize!=0:
                        # dataArr.pop(dataKey)
                        resultArr.append(dataValue);
                        resultSize +=1;

            #再查询出所有的或结果
            if selectOrSize>0:
                for dataKey,dataValue in enumerate(dataArr):
                    #对每个数据进行匹配
                    #每个条件进行匹配
                    for key,selectValue in enumerate(selectOrArr):
                        singleCheck=0;
                        for singleKey,singleValue in selectValue.items():
                            thisKey=singleKey.strip('~')
                            if thisKey in dataValue.keys():
                                if MatchUtil.match(singleValue, dataValue[thisKey]):
                                    resultArr.append(dataValue);
                                    resultSize+=1;
                                    singleCheck+=1;
                        if singleCheck!=0:
                            break;

            return resultArr
        else:
            return Consts.noneArr

    def selectNormal(self, *args):
        data=args[0]
        resultArr=self.get_selectedArray(data['where'])
        return resultArr

    def insertNormal(self,*args):
        rows=""
        data=args[2]
        tableName=args[1]
        times = ClockUtil.getTimes()
        try:
            fileName=self.getFileName(tableName)
            ##首先读取文件内容sudo 这一部分需要优化，要不然每次都把文件读出到内存的话会很耗内存以及性能
            fileState=os.path.exists(fileName)
            text=""
            dataArr=[]
            if(fileState):
                myNosqlfile =  codecs.open(fileName, "r")
                text = myNosqlfile.read()
                myNosqlfile.close()
                length=len(text)-1
                if length>0:
                    dataArr=json.loads(text)
                    text=text[:length]
            ##先写入内存
            GF=GnosqlFileListUtil();
            memoryStr='{"guid":"'+times+'",'+data+"}"
            memoryData=json.loads(memoryStr)
            GF.addMemoryDict(memoryData,tableName)

            ##写入文件操作
            myNosqlfile =  codecs.open(fileName, "w")
            if text=="":
                text += '[{'
            else:
                text += ',{'
            text=text+'"guid":"'+times+'",';
            text=text+data;
            text += '}'
            text += "]"
            myNosqlfile.write(text)
            myNosqlfile.close()
            rows=times;
        except BaseException as e:
            print(repr(e))
            rows='IOError'
        return rows

    def deleteNormal(self,*args):
        rows=""
        dataStr=args[0]["where"]
        tableName=args[1]
        times = ClockUtil.getTimes()
        try:
            result=self.get_selectedArray(dataStr);
            if result!=Consts.noneArr:
                GF=GnosqlFileListUtil();
                #这里是从内存里面获取到数据字典
                dataDict=GF.getMemoryDictDataReal(tableName)['data']
                dataArr=dataStr.split(Consts.thisSeparaterArr)
                tableName=dataArr[0];
                fileName=self.getFileName(tableName)
                data="["+dataArr[1];
                fileState=os.path.exists(fileName)
                text=""
                dataArr=[]
                if(fileState):
                    myNosqlfile = codecs.open(tableName+".gnql", "r");
                    text=myNosqlfile.read()
                    myNosqlfile.close()
                    dataArr=json.loads(text)

                    for key2,value2 in enumerate(result):
                        for key,value in enumerate(dataArr):
                            if value['guid']==value2['guid']:
                                dataDict.pop(key)
                                dataArr.pop(key)

                    if len(dataArr)>0 :
                        text=json.dumps(dataArr)
                    else:
                        text=""
                    myNosqlFile = codecs.open(self.getFileName(tableName), "w")
                    myNosqlFile.write(text)
                    myNosqlFile.close()
                    rows=Consts.deleted
            else:
                rows=Consts.nonDeleted
        except BaseException as e:
                print(repr(e))
                rows=Consts.IOError
        return rows

    def updateNormal(self,*args):
        rows=""
        dataStr=args[0]['where']
        updateArr=args[0]['update']
        tableName=args[1]
        times = ClockUtil.getTimes()
        try:
            result=self.get_selectedArray(dataStr);
            if result!=Consts.none:

                memeryData=GF=GnosqlFileListUtil();
                #这里是从内存里面获取到数据字典
                dataDict=GF.getMemoryDictDataReal(tableName)['data']

                dataArr=dataStr.split(Consts.thisSeparaterArr)
                tableName=dataArr[0];
                fileName=self.getFileName(tableName)
                data="["+dataArr[1];
                fileState=os.path.exists(fileName)
                text=""
                dataArr=[]
                if(fileState):

                    myNosqlfile = codecs.open(fileName, "r");
                    text=myNosqlfile.read()
                    myNosqlfile.close()
                    dataArr=json.loads(text)

                    for key2,value2 in enumerate(result):
                        for key,value in enumerate(dataArr):
                            if value['guid']==value2['guid']:
                                for key3,value3 in updateArr.items():
                                    dataDict[key][key3]=value3;
                                    dataArr[key][key3]=value3;


                    text=json.dumps(dataArr)
                    myNosqlFile = codecs.open(self.getFileName(tableName), "w")
                    myNosqlFile.write(text)
                    myNosqlFile.close()
                    rows=Consts.updated
            else:
                rows=Consts.nonUpdated
        except BaseException as e:
            print(repr(e))
            rows=Consts.IOError
        return rows

    @staticmethod
    def getFileName(tableName):
        return Consts.path+tableName+Consts.fileSuffix

