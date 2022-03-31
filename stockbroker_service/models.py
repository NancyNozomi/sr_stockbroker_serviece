import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ptk
from scipy.ndimage import gaussian_filter1d
import baostock as bs
import os


class Stock(object):

    def __init__(self, name, DB):
        self.name = name
        self.DB = DB
        self.date_list = []
        self.get_date()
        self.current_time = datetime.datetime.now().strftime('%Y%m%d')[2:]

    def get_stock_period(self, end_time):
        stock_price = {}
        index = self.date_list.index(end_time)
        start_time = self.date_list[index - 30]
        rs = bs.query_history_k_data_plus(
            "sh.%s" % self.name[-6:], "date, close",
            start_date=self.time_cvt(start_time, 1),
            end_date=self.time_cvt(end_time, 1)
        )
        for i in range(len(rs.data)):
            date = rs.data[i][0][5:]
            stock_price[date] = float(rs.data[i][1])
        return stock_price

    def get_stock_current(self):
        stock_price = {}
        index = self.date_list.index(self.current_time)
        start_time = self.date_list[index - 7]
        rs = bs.query_history_k_data_plus(
            "sh.%s" % self.name[-6:], "time, close",
            start_date=self.time_cvt(start_time, 1),
            end_date=self.time_cvt(self.current_time, 1),
            frequency="5"
        )
        for i in range(len(rs.data)):
            date = self.time_cvt(rs.data[i][0], 0)
            stock_price[date] = float(rs.data[i][1])
        return stock_price

    def get_date(self):
        for y in range(15, 23):
            for m in range(1, 13):
                for d in range(1, 32):
                    t = "%02d%02d%02d" % (y, m, d)
                    if is_valid_date(t):
                        self.date_list.append(t)
                        if t == datetime.datetime.now().strftime('%Y%m%d')[2:]:
                            return

    @staticmethod
    def draw_period(stock_data, path="./stockbroker_service/static/images"):
        value = list(stock_data.values())
        time = list(stock_data.keys())
        x = range(len(value))
        plt.ion()
        plt.figure(num=0, facecolor='#242424', edgecolor='#888888', figsize=(8, 6))
        ax = plt.axes()
        ax.set_facecolor("#333333")
        plt.plot(x, value, marker="o", markersize=3, color="#8DCB89", linewidth=1, linestyle='-')
        price = gaussian_filter1d(value, 3)
        plt.plot(x, price, color='#888888', linewidth=1, linestyle='--')
        plt.grid(axis="y", linestyle='-.', linewidth=0.5)
        plt.xticks(x, time, rotation=45, color="white")
        plt.yticks(price, color="white")
        ax.xaxis.set_major_locator(ptk.MultipleLocator(base=1))
        value_axis = max(int((np.array(value).max() - np.array(value).min()) * 10) / 100, 0.02)
        ax.yaxis.set_major_locator(ptk.MultipleLocator(base=value_axis))
        plt.savefig(os.path.join(path, ".stock_period.png"), format="png")
        plt.clf()
        plt.close("all")

    @staticmethod
    def draw_current(stock_data, path="./stockbroker_service/static/images"):
        value = list(stock_data.values())
        time = list(stock_data.keys())
        x = range(len(value))
        plt.ion()
        plt.figure(num=0, facecolor='#242424', edgecolor='#888888', figsize=(8, 6))
        ax = plt.axes()
        ax.set_facecolor("#333333")
        plt.plot(x, value, marker="o", markersize=3, color="#8DCB89", linewidth=1, linestyle='-')
        price = gaussian_filter1d(value, 3)
        plt.plot(x, price, color='#888888', linewidth=1, linestyle='--')
        plt.grid(axis="y", linestyle='-.', linewidth=0.5)
        plt.xticks(x, time, rotation=30, color="white")
        plt.yticks(price, color="white")
        ax.xaxis.set_major_locator(ptk.MultipleLocator(base=20))
        value_axis = max(int((np.array(value).max() - np.array(value).min()) * 10) / 100, 0.02)
        ax.yaxis.set_major_locator(ptk.MultipleLocator(base=value_axis))
        plt.savefig(os.path.join(path, ".stock_current.png"), format="png")
        plt.clf()
        plt.close("all")

    @staticmethod
    def time_cvt(time_input, label):
        """
            label 0: "20220321093500000" -> "03-21 09:35"
            label 1: "220321" -> "2022-03-21"
            label -1: "2022-03-21" -> "220321"
        """
        if label == 0:
            time_output = ""
            time_output += time_input[4:6]
            time_output += "-"
            time_output += time_input[6:8]
            time_output += " "
            time_output += time_input[8:10]
            time_output += ":"
            time_output += time_input[10:12]
            return time_output
        elif label == 1:
            time_output = "20"
            time_output += time_input[0:2]
            time_output += "-"
            time_output += time_input[2:4]
            time_output += "-"
            time_output += time_input[4:6]
            return time_output
        elif label == -1:
            time_output = time_input.replace("-", "")[2:]
            return time_output
        else:
            return -1


class Usr(object):

    def __init__(self, name, password, stock_list, DB):
        self.name = name
        self.password = password
        self.stock_list = stock_list
        self.DB = DB
        self.balance_Yuan = 0
        self.balance_JnF = 0
        self.login_state = self.login()
        if self.login_state >= 0:
            bs.login()
            self.get_balance_info()
            self.stock = {}
            """
            stock = {stock_name: {num: num, obj: Stock]}
            """
            self.get_stock_info()
            self.get_stock_obj(DB)

    def login(self):
        usr_list = []
        cur = self.DB.cursor()
        sql = "select name from account"
        cur.execute(sql)
        select = cur.fetchall()
        for (item,) in select:
            usr_list.append(item)
        if self.name not in usr_list:
            sql = "insert into account (name, password) values ('%s', '%s')" % (self.name, self.password)
            cur.execute(sql)
            self.DB.commit()
            cur.close()
            return True
        else:
            sql = "select password from account where name = '%s'" % self.name
            cur.execute(sql)
            select = cur.fetchall()
            cur.close()
            if self.password == select[0][0]:
                return True
            else:
                return False

    def get_stock_info(self):
        cur = self.DB.cursor()
        sql_stock = ""
        for stock_name in self.stock_list:
            sql_stock += "%s, " % stock_name
        sql = "select " + sql_stock[:-2] + " from account where name = '%s'" % self.name
        cur.execute(sql)
        select = cur.fetchall()
        for i in range(len(self.stock_list)):
            self.stock[self.stock_list[i]] = {}
            self.stock[self.stock_list[i]]["num"] = select[0][i]
        cur.close()

    def get_balance_info(self):
        cur = self.DB.cursor()
        sql = "select balance from account where name = '%s'" % self.name
        cur.execute(sql)
        select = cur.fetchall()
        balance = select[0][0]
        cur.close()
        self.balance_Yuan = int(np.floor(balance))
        self.balance_JnF = int((balance - self.balance_Yuan) * 100)

    def get_stock_obj(self, DB):
        for stock_name in self.stock_list:
            self.stock[stock_name]["obj"] = Stock(stock_name, DB)

    def buy_stock(self, stock, num, current_price):
        transaction_amount = int(current_price * num * 100)
        if self.balance_Yuan * 100 + self.balance_JnF < transaction_amount:
            return -1
        else:
            self.balance_Yuan -= transaction_amount // 100
            self.balance_JnF -= transaction_amount % 100
            balance = self.balance_Yuan + self.balance_JnF / 100
            self.stock[stock.name]["num"] += num
            cur = self.DB.cursor()
            sql = "UPDATE account SET balance = %.2f, %s = %d WHERE name = '%s'" % \
                  (balance, stock.name, self.stock[stock.name]["num"], self.name)
            cur.execute(sql)
            self.DB.commit()
            return 0

    def sell_stock(self, stock, num, current_price):
        transaction_amount = int(current_price * num * 100)
        if self.stock[stock.name]["num"] < num:
            return -2
        else:
            self.balance_Yuan += transaction_amount // 100
            self.balance_JnF += transaction_amount % 100
            balance = self.balance_Yuan + self.balance_JnF / 100
            self.stock[stock.name]["num"] -= num
            cur = self.DB.cursor()
            sql = "UPDATE account SET balance = %.2f, %s = %d WHERE name = '%s'" % \
                  (balance, stock.name, self.stock[stock.name]["num"], self.name)
            cur.execute(sql)
            self.DB.commit()
            return 0


def time_string2array(time_input):
    """
        "220307" -> [2022, 3, 7]
    """
    time_array = np.zeros((3,), np.int16)
    time_array[0] = int(time_input[0:2]) + 2000
    time_array[1] = int(time_input[2:4])
    time_array[2] = int(time_input[4:6])
    return time_array


def is_valid_date(t):
    t = time_string2array(t)
    try:
        datetime.date(t[0], t[1], t[2])
    except:
        return False
    else:
        return True
