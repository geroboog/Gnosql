from flask import jsonify


class ResponseUtil(object):
    def __init__(self): pass

    @staticmethod
    def getResponse(code, data, msg):
        if "rows" in data.keys():
            result = {"code": code, "data": data['rows'], "msg": msg}
            return result
        else:
            result = {"code": code, "data": data, "msg": msg}
            return result

    @staticmethod
    def getResponseNormal(code, data, msg):
        result = {"code": code, "data": data, "msg": msg}
        return result

    @staticmethod
    def getCORSResponse(result):
        response = jsonify(result)
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        response.headers['Access-Control-Allow-Credentials'] = 'true';
        return response;

    @staticmethod
    def setCORSResponse(result):
        result.headers['Access-Control-Allow-Origin'] = '*'
        result.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
        result.headers['Access-Control-Allow-Headers'] = 'x-requested-with'
        result.headers['Access-Control-Allow-Credentials'] = 'true';
        return result;
