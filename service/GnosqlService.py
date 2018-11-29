from dao.GnosqlDao import GnosqlDao
from util import ClockUtil, GrammerConstructor
from util.ResponseUtil import ResponseUtil
from util import PageUtil
from flask import session, request
import json
import time
from util import Consts
from util.GnosqlTokenListUtil import GnosqlTokenListUtil
import threading
from util.ClockUtil import ClockUtil
import os, re


class GnosqlService(object):
    gnosqlDao = type(None)
    GT = type(None)

    # 定义构造方法
    def __init__(self):
        self.gnosqlDao = GnosqlDao()
        self.GT = GnosqlTokenListUtil()

    def checkUserToken(self, data):
        dataKeys = data.keys()
        if Consts.gnosqlId in dataKeys and Consts.where in dataKeys and Consts.token in dataKeys:
            gnosqlId = data[Consts.gnosqlId]
            referer = request.referrer
            check = True;
            if Consts.appName in dataKeys and referer is None:
                check = self.checkAppNameInList(gnosqlId, data[Consts.appName])
            elif not Consts.appName in dataKeys and not referer is None:
                check = self.checkAppIpInList(gnosqlId, referer)
            else:
                return False

            token = data[Consts.token];
            dataRow = self.getGnosqlInfoFun(gnosqlId);
            thisToken = dataRow[Consts.rows][0][Consts.token];
            if token == thisToken and check:
                t = threading.Thread(target=recordTable, args=(data,), name='recordTable')
                t.start()
                t.join()
                return True
            else:
                return False
        else:
            return False

    # 查看appIp是否存在
    def checkAppIpInList(self, gnosqlId, referer):
        selectObj = {}
        dataObject2 = {};
        result = False;
        dataObject2["@gnosqlId"] = gnosqlId;
        dataObject2["@appIp"] = "%%";
        dataStr2 = "gnosqlIp@" + json.dumps([dataObject2]);
        selectObj[Consts.where] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        for row in rows[Consts.rows]:
            thisAppIp = row[Consts.appIp]
            if re.match(r"^" + thisAppIp + ".*", referer):
                result = True;
                break;
        return result;

    # 查看appName是否存在
    def checkAppNameInList(self, gnosqlId, appName):
        selectObj = {}
        dataObject2 = {};
        result = False;
        dataObject2["@gnosqlId"] = gnosqlId;
        dataObject2["@appName"] = "%%";
        dataStr2 = "gnosqlIp@" + json.dumps([dataObject2]);
        selectObj[Consts.where] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        for row in rows[Consts.rows]:
            if row[Consts.appName] == appName:
                result = True;
                break;
        return result;

    def getUsername(self):
        return request.cookies.get(Consts.sessionUsername)

    def getTableName(self, dataStr):
        tableName = dataStr[Consts.where]
        gnosqlId = dataStr[Consts.gnosqlId]
        return gnosqlId + "/" + gnosqlId + tableName

    # 查询数据
    def basicfunctin(self, data, CRUDfunction, successMsg):
        result = {}
        code = 0
        msg = "";
        if not self.checkUserToken(data):
            msg = Consts.needToken
            code = 100
        else:
            if data == type(None):
                msg = Consts.msgEmptyGNQL
            else:
                data[Consts.where] = self.getTableName(data)
                rows = CRUDfunction(data);
                result[Consts.rows] = rows
                msg = Consts.msgSuccess;
        response = ResponseUtil.getResponse(code, result, msg)
        return response

    def basicfunctin2(self, dataStr, CRUDfunction, successMsg):
        result = {}
        code = 0
        msg = "";
        if not self.checkUserToken(dataStr):
            msg = Consts.checkYourParameters
            code = 100
        else:
            dataStr[Consts.where] = self.getTableName(dataStr)
            result = self.progressDataStr(result, dataStr, CRUDfunction)
            msg = Consts.msgSuccess;

        response = ResponseUtil.getResponse(code, result, msg)
        return response

    def select(self, data):
        return self.basicfunctin(data, self.gnosqlDao.selectNormal, Consts.msgSuccess)

    def insert(self, dataStr):
        return self.basicfunctin2(dataStr, self.gnosqlDao.insertNormal, Consts.msgSuccess)

    def delete(self, dataStr):
        return self.basicfunctin2(dataStr, self.gnosqlDao.deleteNormal, Consts.msgSuccess)

    def update(self, dataStr):
        return self.basicfunctin2(dataStr, self.gnosqlDao.updateNormal, Consts.msgSuccess)

    def progressDataStr(self, result, dataStr, processFunc):
        # 首先定义语法：现在主流的语法使用一般是json格式的语言
        # 我定义的nosql数据库为文档式数据库以一个集合为单位：如语法:user@{"userId":1,"userName":"小曾"}
        dataArr = dataStr[Consts.where].split(Consts.thisSeparaterArr)
        code = 0
        try:
            tableName = dataArr[0];
            data = dataArr[1];
            data = data.strip(Consts.lastSeparater);
            data = data.strip(Consts.firstSeparater);
            if dataArr[0] == type(None) or dataArr[1] == type(None):
                msg = Consts.msgFormat
                code = 100
            else:
                rows = processFunc(dataStr, tableName, data)
                result[Consts.rows] = rows
                msg = Consts.msgSuccess
        except BaseException as e:
            msg = Consts.msgFormat
            code = 100

        result[Consts.msg] = msg
        result[Consts.code] = code
        return result

    def getGnosqlInfoFun(self, gnosqlId):
        selectObj = {};
        dataObject = {"@gnosqlId": gnosqlId};
        dataStr = "gnosql@" + json.dumps([dataObject]);
        selectObj[Consts.where] = dataStr;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        return rows;

    def getUserTableList(self, gnosqlId):
        tableList = [];
        for filename in os.listdir(Consts.path + gnosqlId):
            if re.match(r"^" + gnosqlId + ".*", filename) and not re.match(r".*gnosql_access.*", filename):
                thisFilename = filename.split(Consts.fileSuffix)[0].split(gnosqlId)[1]
                tableList.append(thisFilename)
        return tableList;



# 新线程执行的代码:
def recordTable(data):
    gnosqlId = data[Consts.gnosqlId];
    tableName = data[Consts.where].split("@")[0];
    today = ClockUtil.getToday();
    gd = GnosqlDao()
    selectObj = {};
    gs = GnosqlService();
    tableFullName = gnosqlId + "gnosql_access@"
    dataObject = {"@gnosqlId": gnosqlId, "@tableName": tableName, "@date": today};
    dataStr = GrammerConstructor.constructTableGrammar(gnosqlId, "gnosql_access", [dataObject]);
    selectObj[Consts.where] = dataStr;
    rows = gs.progressDataStr({}, selectObj, gd.selectNormal);
    if len(rows[Consts.rows]) > 0:
        updateObj = {}
        row = rows[Consts.rows][0];
        row["count"] += 1
        updateObj[Consts.where] = dataStr;
        updateObj[Consts.update] = row
        rows = gs.progressDataStr({}, updateObj, gd.updateNormal);
    else:
        dataObject = {Consts.gnosqlId: gnosqlId, "tableName": tableName, "date": today, "count": 1};
        dataStr = GrammerConstructor.constructTableGrammar(gnosqlId, "gnosql_access", [dataObject]);
        selectObj[Consts.where] = dataStr;
        rows = gs.progressDataStr({}, selectObj, gd.insertNormal);
