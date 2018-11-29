import json
from controller import controllers
from flask import request, session, jsonify, render_template
from service import GnosqlService
from service.GnosqlUserService import GnosqlUserService
from util.ResponseUtil import ResponseUtil
from util import Consts

# 用户主页面
@controllers.route('/gnosqlUser')
def gnosqlUser():
        return render_template('/gnosql/index.html')

# 数据库信息页面
@controllers.route('/gnosqlUser/gnosql_info')
def gnosql_info():
    return checkLogin('/gnosql/main/gnosql_info.html')


# 数据分析页面
@controllers.route('/gnosqlUser/data_analysis')
def data_analysis():
    return checkLogin('/gnosql/main/data_analysis.html')


# 关于我们页面
@controllers.route('/gnosqlUser/about_us')
def about_us():
    return checkLogin('/gnosql/main/about_us.html')


# 主框架页面
@controllers.route('/gnosqlUser/main')
def gnosqlUserMain():
    return checkLogin('/gnosql/main/main.html')

def checkLogin(page):
    if Consts.sessionUsername in session.keys():
        return render_template(page);
    else:
        return render_template('/gnosql/index.html');

# 用户登录页面
@controllers.route('/gnosqlUser/userLogin', methods=['POST'])
def userLogin():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    username = jsonData['username']
    password = jsonData["password"]
    gnosqlObj = GnosqlUserService()
    result = gnosqlObj.userLogin(username, password)
    return ResponseUtil.setCORSResponse(result)


# 用户注册页面
@controllers.route('/gnosqlUser/userSignUp', methods=['POST'])
def userSignUp():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    username = jsonData['username']
    password = jsonData["password"]
    gnosqlUserObj = GnosqlUserService()
    result = gnosqlUserObj.userSignUp(username, password)
    return ResponseUtil.getCORSResponse(result)


# 创建数据库
@controllers.route('/gnosqlUser/createGnosql', methods=['POST'])
def createGnosql():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlName = jsonData["gnosqlName"];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.createGnosql(gnosqlName);
    return ResponseUtil.getCORSResponse(result);


# 获取数据库列表
@controllers.route('/gnosqlUser/getGnosqlList', methods=['POST'])
def getGnosqlList():
    a = request.get_data();
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.getGnosqlList();
    return ResponseUtil.getCORSResponse(result);


# 生成Token
@controllers.route('/gnosqlUser/generateToken', methods=['POST'])
def generateToken():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    username = jsonData['username'];
    gnosqlId = jsonData["gnosqlId"];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.generateToken(username, gnosqlId);
    return ResponseUtil.getCORSResponse(result);


# 增加绑定的IP
@controllers.route('/gnosqlUser/addGnosqlAppIp', methods=['POST'])
def addGnosqlAppIp():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    appIp = jsonData["appIp"];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.addGnosqlAppIp(gnosqlId, appIp);
    return ResponseUtil.getCORSResponse(result);


# 增加APP名称
@controllers.route('/gnosqlUser/addGnosqlAppName', methods=['POST'])
def addGnosqlAppName():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    appName = jsonData["appName"];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.addGnosqlAppName(gnosqlId, appName);
    return ResponseUtil.getCORSResponse(result);



# 删除绑定的IP
@controllers.route('/gnosqlUser/deleteGnosqlAppIp', methods=['POST'])
def deleteGnosqlAppIp():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    appIp = jsonData["appIp"];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.deleteGnosqlAppIp(gnosqlId, appIp);
    return ResponseUtil.getCORSResponse(result);


# 删除APP名称
@controllers.route('/gnosqlUser/deleteGnosqlAppName', methods=['POST'])
def deleteGnosqlAppName():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    appName = jsonData["appName"];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.deleteGnosqlAppName(gnosqlId, appName);
    return ResponseUtil.getCORSResponse(result);

# 获取表信息
@controllers.route('/gnosqlUser/getGnosqlTableInfo', methods=['POST'])
def getGnosqlTableInfo():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.getGnosqlTableInfo(gnosqlId);
    return ResponseUtil.getCORSResponse(result);

# 获取数据库信息
@controllers.route('/gnosqlUser/getGnosqlInfo', methods=['POST'])
def getGnosqlInfo():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.getGnosqlInfo(gnosqlId);
    return ResponseUtil.getCORSResponse(result);

# 获取表访问信息
@controllers.route('/gnosqlUser/getGnosqlDataAnalysis', methods=['POST'])
def getGnosqlDataAnalysis():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    startDate = jsonData['startDate'];
    endDate = jsonData['endDate'];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.getGnosqlDataAnalysis(gnosqlId,startDate,endDate);
    return ResponseUtil.getCORSResponse(result);

# 获取表访问类别信息
@controllers.route('/gnosqlUser/getGnosqlDataType', methods=['POST'])
def getGnosqlDataType():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    gnosqlId = jsonData['gnosqlId'];
    startDate = jsonData['startDate'];
    endDate = jsonData['endDate'];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.getGnosqlDataType(gnosqlId,startDate,endDate);
    return ResponseUtil.getCORSResponse(result);


# 获取所有表访问信息
@controllers.route('/gnosqlUser/getGnosqlAllDataAnalysis', methods=['POST'])
def getGnosqlAllDataAnalysis():
    a = request.get_data();
    jsonData = json.loads(a.decode("utf-8"));
    startDate = jsonData['startDate'];
    endDate = jsonData['endDate'];
    gnosqlUserObj = GnosqlUserService();
    result = gnosqlUserObj.getGnosqlAllDataAnalysis(startDate,endDate);
    return ResponseUtil.getCORSResponse(result);

#
# @controllers.route('/gnosql/checkToken', methods=['POST'])
# def checkToken():
#         a = request.get_data()
#         jsonData = json.loads(a.decode("utf-8"))
#         gnosqlId = jsonData['gnosqlId']
#         token = jsonData['token']
#         gnosqlUserObj = GnosqlService.GnosqlUserService()
#         result = gnosqlUserObj.checkToken(gnosqlId,token)
#         return ResponseUtil.getCORSResponse(result)

