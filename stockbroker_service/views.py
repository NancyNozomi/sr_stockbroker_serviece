from django.http import HttpResponseRedirect
from django.shortcuts import render
import stockbroker_service.controller as controller


def index(request):
    controller.Initializer()
    if request.method == "POST":
        v = {'project_header': 'Stockbroker service',
             "login_state": "Your password is wrong \n please re-login."
             }
    else:
        v = {'project_header': 'Stockbroker service',
             "login_state": "If you do not have an account \n this login will automatically register it for you."
             }
    return render(request, 'index.html', v)


def log_in(request):
    if request.method == "POST":
        c = controller.LogInController(request.POST)
        if c.login_state:
            v = {'project_header': 'Stockbroker service', "login_state": "list"}
        else:
            v = {'project_header': 'Stockbroker service', "login_state": "index"}
        return render(request, 'login.html', v)


def get_usr_info(request):
    c = controller.GetUsrInfoController()
    v = {'project_header': c.usr_info.name,
         "stock_list": c.stock_name_list
         }
    return render(request, "list.html", v)


def visual(request):
    if request.method == "POST":
        c = controller.VisualController(request.POST)
        v = {'project_header': c.usr_info.name,
             'stock_name': c.stock_name,
             "stock_num": c.usr_info.stock[c.stock_code]["num"]
        }
        return render(request, "visual.html", v)


def trade_request(request):
    if request.method == "POST":
        c = controller.TradeRequestController(request.POST)
        buy_num = int(c.form.data["buy_num"]) if c.form.data["buy_num"] != '' else 0
        sell_num = int(c.form.data["sell_num"]) if c.form.data["sell_num"] != '' else 0
        stock_name = c.stock_name
        usr_info = c.usr_info
        buy_num -= sell_num
        current_price = c.current_price
        if buy_num >= 0:
            conf_info = "You will buy the stock %s for %d with price %.2f" % (stock_name, buy_num, current_price)
        else:
            conf_info = "You will sell the stock %s for %d with price %.2f" % (stock_name, -buy_num, current_price)
        v = {
            'project_header': usr_info.name,
            "trade": 0,
            "conf_info": conf_info,
            "stock_name": stock_name,
            "buy_num": buy_num,
            "stock": c.stock_num,
            "balance": usr_info.balance_Yuan + usr_info.balance_JnF / 1e2,
            "current_price": current_price
        }
        return render(request, "person.html", v)


def trade(request):
    if request.method == "POST":
        c = controller.TradeController(request.POST)
        if c.buy_num >= 0:
            state = c.usr_info.buy_stock(c.usr_info.stock[c.stock_code]["obj"], c.buy_num, c.current_price)
        else:
            state = c.usr_info.sell_stock(c.usr_info.stock[c.stock_code]["obj"], -c.buy_num, c.current_price)
        c.get_stock_num()
        if state == 0:
            v = {
                'project_header': c.usr_info.name,
                "trade": 1,
                "conf_info": "Trade finished!",
                "stock_name": c.stock_name,
                "buy_num": c.buy_num,
                "stock": c.stock_num,
                "balance": c.usr_info.balance_Yuan + c.usr_info.balance_JnF / 1e2
            }
            return render(request, "person.html", v)
        else:
            v = {
                'project_header': c.usr_info.name,
                "trade": 1,
                "conf_info": "Trade failed!",
                "stock_name": c.stock_name,
                "buy_num": c.buy_num,
                "stock": c.stock_num,
                "balance": c.usr_info.balance_Yuan + c.usr_info.balance_JnF / 1e2
            }
            return render(request, "person.html", v)


def query(request):
    if request.method == "POST":
        c = controller.QueryController(request.POST)
        v = {'project_header': c.usr_info.name,
             'stock_name': c.stock_name,
             "stock_num": c.usr_info.stock[c.stock_code]
        }
        return render(request, "query.html", v)
