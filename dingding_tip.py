import requests
import simplejson
import tushare as ts
from datetime import datetime
import time
import configparser

class dingding:
    def __init__(self,data=None):
        self.url = 'https://oapi.dingtalk.com/robot/send?access_token=30ab91120372f39d361f173762d050797d04eb548d79faadc78a6eaf5c5dfb24'
        self.header = {
                       'Content-type':'application/json',
		               'Charset':'utf-8'
		               }
        self.data = data

    def tips(self):
        sendData = simplejson.dumps(self.data)
        requests.post(self.url, data = sendData, headers =self.header)

class readConf:
    def __init__(self,iniFile = ''):
        self.iniFile = iniFile
    def readConf(self):
        conf = configparser.ConfigParser()
        conf.read(self.iniFile)
        code = conf.get("group_a","code")
        sell_price = conf.get("group_a","sell_price")
        buy_price = conf.get("group_a","buy_price")
        return code,sell_price,buy_price

class stockPrice:
    def __init__(self,code = ''):
        self.code = code
    def getStockPrice(self):
        #stock_basics = ts.get_stock_basics()
        real_price = ts.get_realtime_quotes(self.code)
        name = real_price['name'][0]
        price = real_price['price'][0]
        return name,price

class warning(stockPrice,readConf,dingding):
    def __init__(self,confile):
        readConf.__init__(self,confile)
        time_now = datetime.now()
        self.weekd = time_now.isoweekday()
        self.hour = time_now.hour
        self.hm = time_now.strftime('%H-%M')
        self.code, self.sell_price, self.buy_price = readConf.readConf(self)
        self.sell_price = float(self.sell_price)
        self.buy_price = float(self.buy_price)
       # stockPrice.__init__(self)


    def warning(self,n):
        if self.weekd   in range(1,6) :
            if self.hour   in range(13,16) or \
                (self.hm >= '09-30' and self.hm <= '11-30') :
                while True:
                    sname,price = stockPrice.getStockPrice(self)
                    price = float(price)
                    content = ''
                    if price < self.buy_price:
                        content = '%s 实时价格 %s 请注意买入！'%(sname,price)
                        print (content)
                    elif price > self.sell_price:
                        content = '%s 实时价格 %s 请注意卖出！'%(sname,price)
                        print (content)
                    data = {'msgtype': 'text',
                            'text': {'content': content}
                             }
                    msg_dingding = dingding(data)
                    msg_dingding.tips()
                    time.sleep(n)

if __name__ == '__main__':
    warn_dingding = warning('conf.ini')
    warn_dingding.warning(5)



