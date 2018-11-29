from dao import GnosqlDao
from util.ClockUtil import ClockUtil
from util.ResponseUtil import ResponseUtil
from util import PageUtil
from flask import session, jsonify, make_response
import json
import os
import time
from util import Consts
from util.GnosqlTokenListUtil import GnosqlTokenListUtil
from service.GnosqlService import GnosqlService
from util import FileInfoUtil


class GnosqlUserService(object):
    gnosqlDao = type(None)

    # 定义构造方法
    def __init__(self):
        self.gnosqlDao = GnosqlDao.GnosqlDao()

    def userLogin(self, username, password):
        result = {}
        code = 0
        msg = ""
        rows = self.gnosqlDao.selectNormal(
            {"where": self.constructSysTableGrammar(Consts.user, {"@username": username})});
        if rows == Consts.noneArr:
            msg = Consts.userUnExist
            code = 2
        else:
            if rows[0]['password'] == password:
                msg = Consts.loginSuccess
                self.saveLogin(rows[0])
                session[Consts.sessionUsername] = username
            else:
                msg = Consts.passwordError
                code = 1
        ##然后判断用户密码
        result['rows'] = ""
        result = ResponseUtil.getResponse(code, result, msg)

        response = make_response(jsonify(result))
        if code == 0:
            response.set_cookie(Consts.sessionUsername, username)
        return response

    def userSignUp(self, username, password):
        result = {}
        msg = ""
        rows = self.gnosqlDao.selectNormal(
            {"where": self.constructSysTableGrammar(Consts.user, {"@username": username})});
        if rows != Consts.noneArr:
            msg = Consts.userExist
        else:
            insertObj = {}
            dataStr = self.constructSysTableGrammar(Consts.user, {"username": username, "password": password});
            insertObj["where"] = dataStr
            gs = GnosqlService()
            rows = gs.progressDataStr({}, insertObj, self.gnosqlDao.insertNormal)
            msg = Consts.SignUpSuccess

        ##然后判断用户密码
        response = ResponseUtil.getResponse(0, result, msg)
        return response

    def saveLogin(self, userData):
        GT = GnosqlTokenListUtil()
        # 存储登录状态
        GT.setLoginDict(userData, userData['username'])

    def checkToken(self, username, token):
        result = {}
        msg = ""
        GT = GnosqlTokenListUtil()
        isExist = GT.existToken(token, username)
        if not isExist:
            msg = Consts.tokenUnExist
        else:
            msg = Consts.tokenExist

        ##然后判断用户密码
        response = ResponseUtil.getResponse(0, result, msg)
        return response

    def createGnosql(self, gnosqlName):
        GT = GnosqlTokenListUtil();
        insertObj = {};
        dataObject = {};
        username = session[Consts.sessionUsername];
        gs = GnosqlService();
        dataObject["@username"] = username;
        dataObject["@gnosqlName"] = gnosqlName;
        dataStr = self.constructSysTableGrammar(Consts.gnosql, dataObject);
        insertObj["where"] = dataStr;
        result = gs.progressDataStr({}, insertObj, self.gnosqlDao.selectNormal);

        if len(result['rows']) > 0:
            response = ResponseUtil.getResponse(100, {}, Consts.gnosqlExist);
            return response

        gnosqlId = GT.generateGnosqlId(username);
        token = GT.getToken(username);
        dataObject["username"] = username;
        dataObject["gnosqlName"] = gnosqlName;
        dataObject["gnosqlId"] = gnosqlId;
        dataObject["tableNum"] = 0;
        dataObject["token"] = token;
        dataObject["tableList"] = "";
        dataStr = self.constructSysTableGrammar(Consts.gnosql, dataObject);
        insertObj["where"] = dataStr;
        result = gs.progressDataStr({}, insertObj, self.gnosqlDao.insertNormal);
        response = ResponseUtil.getResponse(result['code'], result, result['msg']);
        if result['code'] == 0:
            mkdir(Consts.path + gnosqlId);
            filePath = Consts.path + gnosqlId + "/" + gnosqlId + "gnosql_access" + Consts.fileSuffix
            fp = open(filePath, 'w')
            fp.write("[]");
            fp.close();
        return response;

    def getGnosqlListFun(self):
        msg = "";
        username = session[Consts.sessionUsername];
        selectObj = {};
        dataObject = {"@username": username};
        dataStr = self.constructSysTableGrammar(Consts.gnosql, dataObject);
        selectObj["where"] = dataStr;
        gs = GnosqlService();
        return gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);

    def getGnosqlList(self):
        result = self.getGnosqlListFun();
        response = ResponseUtil.getResponse(0, result, result['msg']);
        return response;

    def generateToken(self, username, gnosqlId):
        dataObject = {};
        insertObj = {};
        updateObj = {};
        GT = GnosqlTokenListUtil();
        token = GT.getToken(username);
        dataObject["@gnosqlId"] = gnosqlId;
        whereStr = self.constructSysTableGrammar(Consts.gnosql, dataObject);
        updateObj["token"] = token;
        insertObj["where"] = whereStr;
        insertObj["update"] = updateObj;
        gs = GnosqlService();
        result = gs.progressDataStr({}, insertObj, self.gnosqlDao.updateNormal);
        response = ResponseUtil.getResponse(0, result, result['msg']);
        return response;

    def addGnosqlAppIp(self, gnosqlId, appIp):
        GT = GnosqlTokenListUtil();
        result = {};
        msg = "";
        insertObj = {};
        dataObject = {};
        dataObject["gnosqlId"] = gnosqlId;
        dataObject["appIp"] = appIp;
        dataStr = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject);
        insertObj["where"] = dataStr;

        selectObj = {}
        dataObject2 = {};
        dataObject2["@gnosqlId"] = gnosqlId;
        dataObject2["@appIp"] = appIp;
        dataStr2 = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject2);
        selectObj["where"] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        if len(rows["rows"]) < 1:
            result = gs.progressDataStr({}, insertObj, self.gnosqlDao.insertNormal);
            msg = result["msg"]
        response = ResponseUtil.getResponse(0, result, msg);
        return response;

    def addGnosqlAppName(self, gnosqlId, appName):
        GT = GnosqlTokenListUtil();
        result = {};
        msg = "";
        insertObj = {};
        dataObject = {};
        dataObject["gnosqlId"] = gnosqlId;
        dataObject["appName"] = appName;
        dataStr = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject);
        insertObj["where"] = dataStr;

        selectObj = {}
        dataObject2 = {};
        dataObject2["@gnosqlId"] = gnosqlId;
        dataObject2["@appName"] = appName;
        dataStr2 = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject2);
        selectObj["where"] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        if len(rows["rows"]) < 1:
            result = gs.progressDataStr({}, insertObj, self.gnosqlDao.insertNormal);
            msg = result["msg"]
        response = ResponseUtil.getResponse(0, result, msg);
        return response;

    def deleteGnosqlAppIp(self, gnosqlId, appIp):
        result = {};
        msg = "";
        selectObj = {}
        dataObject2 = {};
        dataObject2["@gnosqlId"] = gnosqlId;
        dataObject2["@appIp"] = appIp;
        dataStr2 = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject2);
        selectObj["where"] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.deleteNormal);
        response = ResponseUtil.getResponse(0, result, msg);
        return response;

    def deleteGnosqlAppName(self, gnosqlId, appName):
        result = {};
        msg = "";
        selectObj = {}
        dataObject2 = {};
        dataObject2["@gnosqlId"] = gnosqlId;
        dataObject2["@appName"] = appName;
        dataStr2 = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject2);
        selectObj["where"] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.deleteNormal);
        response = ResponseUtil.getResponse(0, result, msg);
        return response;

    def getGnosqlTableInfo(self, gnosqlId):
        msg = "";
        rows = [];
        gs = GnosqlService();
        tableNameList = gs.getUserTableList(gnosqlId)
        for tableName in tableNameList:
            try:
                dataObj = {}
                path = self.getFilePath(gnosqlId, tableName);
                dataObj['tableName'] = tableName;
                dataObj['createTime'] = FileInfoUtil.getFileCreateTime(path);
                dataObj['size'] = FileInfoUtil.getFileSize(path);
                dataObj['accessTime'] = FileInfoUtil.getFileAccessTime(path);
            except BaseException as e:
                print(repr(e))
                pass
            rows.append(dataObj)
            msg = Consts.msgSuccess
        response = ResponseUtil.getResponseNormal(0, rows, msg);
        return response;

    def getGnosqlInfo(self, gnosqlId):
        result = {};
        gs = GnosqlService();
        rows = gs.getGnosqlInfoFun(gnosqlId);
        msg = rows["msg"];
        result["gnosqlId"] = rows["rows"][0]["gnosqlId"]
        result["token"] = rows["rows"][0]["token"]
        rows = self.getGnosqlIdList(gnosqlId);
        i = 1
        j = 1
        for row in rows["rows"]:
            if "appIp" in row.keys():
                name = "appIp" + str(i);
                result[name] = row["appIp"];
                i += 1;
            else:
                name = "appName" + str(j);
                result[name] = row["appName"];
                j += 1;

        response = ResponseUtil.getResponseNormal(0, result, msg);
        return response;

    def getGnosqlIdList(self, gnosqlId):
        selectObj = {}
        dataObject2 = {};
        dataObject2["@gnosqlId"] = gnosqlId;
        dataStr2 = self.constructSysTableGrammar(Consts.gnosqlIp, dataObject2);
        selectObj["where"] = dataStr2;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        return rows;

    def getFilePath(self, gnosqlId, tableName):
        return Consts.path + gnosqlId + "/" + gnosqlId + tableName + Consts.fileSuffix;

    ##用于后台构造语法
    def constructTableGrammar(self, gnosqlId, tableName, dataObjectList):
        return Consts.path + gnosqlId + "/" + gnosqlId + tableName + "@" + json.dumps(dataObjectList);

        ##用于后台构造语法

    def constructSysTableGrammar(self, tableName, dataObject):
        return Consts.path + tableName + "@" + json.dumps([dataObject]);

    # 获取大数据分析结果
    def getGnosqlDataAnalysis(self, gnosqlId, startDate, endDate):
        msg = "";
        selectObj = {};
        result = {};
        valueArr = [];
        dataObjectList = [];
        dateArr = None;
        if startDate == "":
            dateArr = ClockUtil.getBeforeTodayList(30);
        else:
            dateArr = ClockUtil.getSomeList(startDate, endDate);

        for date in dateArr:
            dataObject = {"~date": date};
            dataObjectList.append(dataObject);

        value = 0;
        dataStr = self.constructTableGrammar(gnosqlId, "gnosql_access", dataObjectList);
        selectObj["where"] = dataStr;
        gs = GnosqlService();
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
        thisRow = rows["rows"];
        for date in dateArr:
            value = 0;
            for row in thisRow:
                if row['date'] == date:
                    value += row['count'];
            valueArr.append(value)

        result['dateArr'] = dateArr;
        result['valueArr'] = valueArr;
        response = ResponseUtil.getResponseNormal(0, result, msg);
        return response;

    def getGnosqlDataType(self, gnosqlId, startDate, endDate):
        msg = "";
        selectObj = {};
        result = {};
        legendData = [];
        seriesData = [];
        selected = {};
        dateArr = None;
        dataObjectList = [];
        gs = GnosqlService();
        legendData = gs.getUserTableList(gnosqlId)
        if startDate == "":
            dateArr = ClockUtil.getBeforeTodayList(30);
        else:
            dateArr = ClockUtil.getSomeList(startDate, endDate);
        for date in dateArr:
            dataObject = {"~date": date};
            dataObjectList.append(dataObject)

        dataStr = self.constructTableGrammar(gnosqlId, "gnosql_access", dataObjectList);
        selectObj["where"] = dataStr;
        rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);

        i = 0;
        for tableName in legendData:
            value = 0;
            selected[tableName] = i < 6;
            for row in rows["rows"]:
                if tableName == row["tableName"]:
                    value += row["count"];
            obj = {"name": tableName, "value": value};
            seriesData.append(obj);
            i += 1;
        result['legendData'] = legendData;
        result['seriesData'] = seriesData;
        result['selected'] = selected;
        response = ResponseUtil.getResponseNormal(0, result, msg);
        return response;

        # 获取大数据分析结果

    def getGnosqlAllDataAnalysis(self, startDate, endDate):
        gnosqlList = self.getGnosqlListFun();
        gnosqlList = gnosqlList[Consts.rows];
        result = {};
        msg = "";
        dateArr = None;
        if startDate == "":
            dateArr = ClockUtil.getBeforeTodayList(30);
        else:
            dateArr = ClockUtil.getSomeList(startDate, endDate);
        first = True;
        valueArr = [];

        for gnosql in gnosqlList:
            selectObj = {};
            dataObjectList = [];
            gnosqlId = gnosql['gnosqlId'];
            for date in dateArr:
                dataObject = {"~date": date};
                dataObjectList.append(dataObject);

            value = 0;
            dataStr = self.constructTableGrammar(gnosqlId, "gnosql_access", dataObjectList);
            selectObj["where"] = dataStr;
            gs = GnosqlService();
            rows = gs.progressDataStr({}, selectObj, self.gnosqlDao.selectNormal);
            thisRow = rows["rows"];
            i = 0;
            if first:
                for date in dateArr:
                    value = 0;
                    for row in thisRow:
                        if row['date'] == date:
                            value += row['count'];
                    valueArr.append(value)
            else:
                for date in dateArr:
                    value = 0;
                    for row in thisRow:
                        if row['date'] == date:
                            value += row['count'];
                    valueArr[i] += value
                    i += 1;

            first = False;
        result['dateArr'] = dateArr;
        result['valueArr'] = valueArr;
        response = ResponseUtil.getResponseNormal(0, result, msg);
        return response;


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        return False
