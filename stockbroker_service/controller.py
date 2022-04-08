from django import forms
from stockbroker_service.models import Usr
import stockbroker_service.glo as glob
import pymysql
import datetime


class Initializer(object):

    def __init__(self):
        glob.set_value("stock_list", ["stock_600016", "stock_600028", "stock_600029", "stock_600050", "stock_600088"])
        glob.set_value("stock_code2name", {
            "stock_600016": "民生银行",
            "stock_600028": "中国石化",
            "stock_600029": "南方航空",
            "stock_600050": "中国联通",
            "stock_600088": "中视传媒"
        })
        glob.set_value("stock_name2code", {
            "民生银行": "stock_600016",
            "中国石化": "stock_600028",
            "南方航空": "stock_600029",
            "中国联通": "stock_600050",
            "中视传媒": "stock_600088"
        })


class Controller(object):
    
    def __init__(self, post):
        self.form = forms.Form(post) if post is not None else None


class LogInController(Controller):

    def __init__(self, post):
        super(LogInController, self).__init__(post)
        self.DB = pymysql.connect(host="127.0.0.1", user="root", password="1", db="sr")
        glob.set_value("DB", self.DB)
        glob.set_value("usr_info",
                       Usr(self.form.data["name"], self.form.data["password"], glob.get_value("stock_list"), self.DB)
        )
        self.login_state = glob.get_value("usr_info").login_state

class GetUsrInfoController(Controller):
    
    def __init__(self):
        super(GetUsrInfoController, self).__init__(None)
        self.usr_info = glob.get_value("usr_info")
        self.stock_name_list = []
        for stock_name in list(self.usr_info.stock.keys()):
            self.stock_name_list.append(glob.get_value("stock_code2name")[stock_name])


class VisualController(Controller):

    def __init__(self, post):
        super(VisualController, self).__init__(post)
        self.stock_name = self.form.data["name"]
        self.stock_code = glob.get_value("stock_name2code")[self.stock_name]
        self.usr_info = glob.get_value("usr_info")
        stock_current = self.usr_info.stock[self.stock_code]["obj"].get_stock_current()
        self.usr_info.stock[self.stock_code]["obj"].draw_current(stock_current)


class TradeRequestController(Controller):

    def __init__(self, post):
        super(TradeRequestController, self).__init__(post)
        self.stock_name = self.form.data["name"]
        self.stock_code = glob.get_value("stock_name2code")[self.stock_name]
        self.usr_info = glob.get_value("usr_info")
        self.current_price = list(self.usr_info.stock[self.stock_code]["obj"].get_stock_current().values())[-1]
        self.stock_num = {}
        for stock_code in self.usr_info.stock_list:
            self.stock_num[glob.get_value("stock_code2name")[stock_code]] = self.usr_info.stock[stock_code]["num"]


class TradeController(Controller):

    def __init__(self, post):
        super(TradeController, self).__init__(post)
        self.buy_num = int(self.form.data["buy_num"])
        self.stock_name = self.form.data["stock_name"]
        self.stock_code = glob.get_value("stock_name2code")[self.stock_name]
        self.usr_info = glob.get_value("usr_info")
        self.current_price = float(self.form.data["current_price"])
        self.stock_num = {}

    def get_stock_num(self):
        for stock_code in self.usr_info.stock_list:
            self.stock_num[glob.get_value("stock_code2name")[stock_code]] = self.usr_info.stock[stock_code]["num"]


class QueryController(Controller):

    def __init__(self, post):
        super(QueryController, self).__init__(post)
        self.stock_name = self.form.data["name"]
        self.stock_code = glob.get_value("stock_name2code")[self.stock_name]
        self.usr_info = glob.get_value("usr_info")
        self.date = self.form.data["date"][2:] if len(self.form.data["date"]) == 8 else datetime.datetime.now().strftime('%Y%m%d')[2:]
        stock_period = self.usr_info.stock[self.stock_code]["obj"].get_stock_period(self.date)
        self.usr_info.stock[self.stock_code]["obj"].draw_period(stock_period)
