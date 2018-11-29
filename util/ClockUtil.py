import datetime
import time


class ClockUtil(object):
    startTime = type(None)
    endTime = type(None)

    def __init__(self): pass

    def getStartTime(self):
        self.startTime = int(round(time.time() * 1000))

    def printTime(self):
        self.endTime = int(round(time.time() * 1000))
        second = (self.endTime - self.startTime)
        print(second)

    @staticmethod
    def getTimes():
        times = time.time()
        return str(round(times * 1000))

    @staticmethod
    def getToday():
        return time.strftime('%Y-%m-%d', time.localtime(time.time()))

    @staticmethod
    def getBeforeTodayList(num):
        result = [];
        datetime.timedelta();
        now_time = datetime.datetime.now();
        while num >= 0:
            yes_time = now_time + datetime.timedelta(days=-num);
            result.append(yes_time.strftime('%Y-%m-%d'));
            num -= 1;
        return result

    @staticmethod
    def getSomeList(startDate,endDate):
        result = []
        start_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(endDate,"%Y-%m-%d")
        while start_date <= end_date:
            date_str = start_date.strftime("%Y-%m-%d")
            result.append(date_str)
            start_date += datetime.timedelta(days=1)
        return result

    @staticmethod
    def getThisMonth():
        return time.strftime('%Y-%m', time.localtime(time.time()))
