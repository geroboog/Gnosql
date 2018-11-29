import json
from controller import controllers
from flask import request, session, jsonify
from service import GnosqlService
from service import GnosqlUserService
from util.ResponseUtil import ResponseUtil


@controllers.route('/gnosql')
def gnosql():
    return 'The gnosql page'


@controllers.route('/gnosql/select', methods=['POST'])
def select():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    gnosqlObj = GnosqlService.GnosqlService()
    result = gnosqlObj.select(jsonData)
    return ResponseUtil.getCORSResponse(result)


@controllers.route('/gnosql/insert', methods=['POST'])
def insert():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    gnosqlObj = GnosqlService.GnosqlService()
    result = gnosqlObj.insert(jsonData)
    return ResponseUtil.getCORSResponse(result)


@controllers.route('/gnosql/delete', methods=['POST'])
def delete():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    gnosqlObj = GnosqlService.GnosqlService()
    result = gnosqlObj.delete(jsonData)
    return ResponseUtil.getCORSResponse(result)


@controllers.route('/gnosql/update', methods=['POST'])
def update():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    gnosqlObj = GnosqlService.GnosqlService()
    result = gnosqlObj.update(jsonData)
    return ResponseUtil.getCORSResponse(result)


@controllers.route('/gnosql/getUserTableList', methods=['POST'])
def getUserTableList():
    a = request.get_data()
    jsonData = json.loads(a.decode("utf-8"))
    gnosqlObj = GnosqlService.GnosqlService()
    result = gnosqlObj.getUserTableList(jsonData)
    return ResponseUtil.getCORSResponse(result)
