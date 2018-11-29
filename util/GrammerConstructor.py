import json

from util import Consts


def constructTableGrammar(gnosqlId, tableName, dataObjectList):
    return Consts.path + gnosqlId + "/" + gnosqlId + tableName + "@" + json.dumps(dataObjectList);
