import re

class MatchUtil(object):
    def __init__(self):
        pass

    @staticmethod
    def match(data,check):
        thisCheck=0;
        if data!="":
            if data[0]=="%" and data[-1]!="%":#根据mysql查询习惯
                data=data[1:];
                data="^((?!"+data+").*)"+data+"$";
                thisCheck=1;

            elif data[-1]=="%" and data[0]!="%" :
                data=data[:-1];
                data="^"+data+".*";
                thisCheck=1;

            elif data[-1]=="%" and data[0]=="%":
                data=data[1:-1];
                data=".*"+data+".*";
                thisCheck=1;

        if thisCheck==0:
            return data==check;
        else:
            return re.match( r""+data, check);
