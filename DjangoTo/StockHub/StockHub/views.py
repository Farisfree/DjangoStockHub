import base64
import io

# 下面这些库是为了data analysis的绘图包
import matplotlib.pyplot as plt
import pandas as pd
from django.http import HttpResponse
from django.shortcuts import render
from pymysql import Connection

conn = Connection(
    host='localhost',
    port=3306,
    user='stock',
    password='123456',
    autocommit=True
)

conn.select_db('stockhub')
cursor = conn.cursor()
user_type = "2"  # 用来判断用户类型
user_id = "222"
stock_code = ""
stock_name = ""


def login(request):
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        tmp_id = request.POST.get("user_id")
        password = request.POST.get("user_password")
        if tmp_id and password:
            check = cursor.execute(f"select user_type from people where user_id = {tmp_id} and passwd = {password}")
            if check:
                info = cursor.fetchall()

                tmp_type = str(info[0][0])
                tmp_type = str(tmp_type)

                global user_id
                user_id = tmp_id
                global user_type
                user_type = tmp_type

                return render(request, "home.html")
            else:
                warning1 = "Please input the correct user_id and passwd!"
                return render(request, "login.html", {"warning1": warning1})
        else:
            warning1 = "Please input the user_id and passwd, do not leave it empty!"
            return render(request, "login.html", {"warning1": warning1})


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        userid = request.POST.get("user_id")
        user_password = request.POST.get("user_password")
        if userid and user_password:
            check = cursor.execute(f'select * from people where user_id = {userid}')
            if check:
                warning1 = "The user have already exist!"
                return render(request, "register.html", {"warning1": warning1})
            else:
                cursor.execute(f'insert into people(user_id,user_type, passwd) values ({userid},{0},{user_password})')
                return render(request, "login.html")
        else:
            warning1 = "Please input the suitable user_id and user_password! Do not leave it empty!"
            return render(request, "register.html", {"warning1": warning1})


# 注意体一下，在测试的时候 全局变量type 要设置成为字符串的形式(改int也行)
def delete(request):
    cursor.execute("Select * from people")
    data = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    df = pd.DataFrame(data, columns=columns)

    if request.method == "GET":
        if user_type == '2':
            return render(request, 'delete.html', {"AllInformation": data})
        else:
            return render(request, 'refuse.html')

    else:
        userid = request.POST.get("user_id")
        password = request.POST.get("user_password")
        if userid and password:
            check = cursor.execute(f'select * from people where user_id = {userid} and passwd = {password}')
            if check:
                cursor.execute(f'delete from people where user_id = {userid}')
                return render(request, 'delete.html', {"AllInformation": data})
            else:
                warning1 = "Please input the correct user_id and pass_word"
                return render(request, "delete.html", {"warning1": warning1, "AllInformation": data})
        else:
            warning1 = "Do not leave it empty!"
            return render(request, "delete.html", {"warning1": warning1, "AllInformation": data})


def stock_basic_info(request):
    if request.method == 'GET':

        return render(request, "stock_basic_info.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 0)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 0})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 0)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 0})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def collect(request):
    name = (stock_name or stock_code)
    cursor.execute(f"insert into collection(user_id, SecuCode) values ('{user_id}','{name}')")
    return render(request,'successful.html')


def collectInterface(request):
    global user_id
    id = user_id
    cursor.execute(f"Select * from collection where user_id = '{id}'")
    info = cursor.fetchall()
    if info:
        return render(request, "collectInterface.html", {'data': info})
    else:
        warning = 'There is no result'
        return render(request, "collectInterface.html", {'warning': warning})


def stock_daily_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_daily_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 1)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 1})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 1)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 1})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_dividend_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_dividend_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 2)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 2})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 2)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 2})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_fees_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_fees_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 3)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 3})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 3)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 3})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_financial_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_financial_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 4)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 4})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 4)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 4})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_price_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_price_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 5)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 5})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 5)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 5})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_ratios_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_ratios_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 6)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 6})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 6)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 6})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_return_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_return_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 7)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 7})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 7)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 7})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def stock_shares_data(request):
    if request.method == 'GET':
        if user_type == "1" or user_type == "2":
            return render(request, "stock_shares_data.html")
        else:
            return render(request, "searchFail.html")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        if SecuCode:
            info, code = searchTable(SecuCode, True, 8)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 8})
        if Lstknm:
            info, code = searchTable(Lstknm, False, 8)
            if info:
                stock_code = code
                cursor.execute(f"replace into history_record (user_id, record_SecuCode) values ('{user_id}','{code}')")
                return render(request, "show.html", {'data': info, "type": 8})
            else:
                return render(request, "searchFail.html")
        else:
            return render(request, "searchFail.html")


def searchTable(context, feature, num):
    if feature:
        table_name = nameOfTable(num)
        check = cursor.execute(f"select * from {table_name} where SecuCode = '{context}'")
        if check:
            info = cursor.fetchall()
            code = info[0][0]
            return info, code
        else:
            return None

    else:
        table_name = nameOfTable(num)
        check = cursor.execute(f"select {table_name}.* from {table_name} \
                                            join (select distinct stock_basic_info.SecuCode from stock_basic_info\
                                             where Lstknm ='{context}') as tmp using(SecuCode) \
                                              where tmp.SecuCode = {table_name}.Secucode")
        if check:
            info = cursor.fetchall()
            code = info[0][0]
            return info, code
        else:
            return None


def nameOfTable(num):
    if num == 0:
        return "stock_basic_info"
    if num == 1:
        return "stock_daily_data"
    elif num == 2:
        return "stock_dividend_data"
    elif num == 3:
        return "stock_fees_data"
    elif num == 4:
        return "stock_financial_data"
    elif num == 5:
        return "stock_price_data"
    elif num == 6:
        return "stock_ratios_data"
    elif num == 7:
        return "stock_return_data"
    else:
        return "stock_shares_data"


def home(request):
    return render(request, 'home.html')


# 展示所有可以搜索的目录
def search_list(request):
    return render(request, "search_list.html")


def personalCenter(request):
    global user_id
    id = user_id
    cursor.execute(f"select * from people where user_id = '{id}'")
    info = cursor.fetchall()
    return render(request, 'personalCenter.html', {'data': info})


def historyShow(request):
    global user_id
    id = user_id
    cursor.execute(f"Select * from history_record where user_id = '{id}'")
    info = cursor.fetchall()
    return render(request, "historyShow.html", {'data': info})


# myapp/views.py


from django.contrib.auth.decorators import login_required
from .models import UserProfile


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, "profile.html")
#
# import io
# import base64
# import matplotlib.pyplot as plt
#
# def generate_scatter_plot(x, y):
#     # 绘制散点图
#     plt.scatter(x, y)
#     plt.xlabel('date')
#     plt.ylabel('price')
#
#     # 将图形转换为字节流
#     buffer = io.BytesIO()
#     plt.savefig(buffer, format='png')
#     buffer.seek(0)
#
#     # 将图形转换为Base64编码字符串
#     image_base64 = base64.b64encode(buffer.getvalue()).decode()
#
#     # 清空图形
#     plt.clf()
#     plt.close()
#
#     return image_base64
#
# def analysis(request):
#     if request.method == 'GET':
#         return render(request, "analysis.html")
#     else:
#         stock_code = request.POST.get('stock_code')
#         if stock_code:
#             cursor.execute(f"SELECT Date_, Oppr FROM stock_daily_data WHERE SecuCode = '{stock_code}'")
#             data = cursor.fetchall()
#             if data:
#                 dates = [int(date.strftime("%Y%m%d")) for date, _ in data]
#                 values = [value for _, value in data]
#                 image_base64 = generate_scatter_plot(dates, values)
#                 return render(request, 'analysis.html', {'image_base64': image_base64})
#             else:
#                 warning = 'Please input the correct stock code.'
#                 return render(request, 'analysis.html', {'warning': warning})
#         else:
#             warning = 'Do not leave the stock code empty!'
#             return render(request, 'analysis.html', {'warning': warning})
import io
import base64
import matplotlib.pyplot as plt

def generate_line_scatter_chart(x, y):
    # 绘制折线图
    plt.plot(x, y, marker='o', linestyle='-', label='Line')

    # 绘制散点图
    plt.scatter(x, y, marker='o', color='red', label='Scatter')

    plt.xlabel('date')
    plt.ylabel('price')
    plt.legend()

    # 将图形转换为字节流
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)

    # 将图形转换为Base64编码字符串
    image_base64 = base64.b64encode(buffer.getvalue()).decode()

    # 清空图形
    plt.clf()
    plt.close()

    return image_base64

def analysis(request):
    if request.method == 'GET':
        return render(request, "analysis.html")
    else:
        stock_code = request.POST.get('stock_code')
        if stock_code:
            cursor.execute(f"SELECT Date_, Oppr FROM stock_daily_data WHERE SecuCode = '{stock_code}'")
            data = cursor.fetchall()
            if data:
                dates = [int(date.strftime("%Y%m%d")) for date, _ in data]
                values = [value for _, value in data]
                image_base64 = generate_line_scatter_chart(dates, values)
                return render(request, 'analysis.html', {'image_base64': image_base64})
            else:
                warning = 'Please input the correct stock code.'
                return render(request, 'analysis.html', {'warning': warning})
        else:
            warning = 'Do not leave the stock code empty!'
            return render(request, 'analysis.html', {'warning': warning})
