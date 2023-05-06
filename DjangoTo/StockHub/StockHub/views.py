from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import HttpResponse
from pymysql import Connection
import pandas as pd


conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='wu101402',
    autocommit=True
)

conn.select_db('stockhub')
cursor = conn.cursor()
user_type = 2 # 用来判断用户类型
user_id = "222"
stock_code = ""
stock_name = ""





def login(request):
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        tmp_id = request.POST.get("user_id")
        password = request.POST.get("user_password")

        check = cursor.execute(f"select user_type from people where user_id = {tmp_id} and passwd = {password}")

        if check:
            info = cursor.fetchall()

            tmp_type = int(info[0][0])
            tmp_type = str(tmp_type)

            global user_id
            user_id= tmp_id
            global user_type
            user_type = tmp_type

            return render(request, "home.html")
        else:
            return HttpResponse("错误")


# search 这一部分有一点疑问 ： 我们是一个表一个function 还是中间还有一个跳转界面来决定展示哪一部分
# (存疑 回学校跟你说)
# def search(request):
#     if request.method == 'GET':
#         return render(request, "search.html", {"user_type": user_type})
#
#     stock_code = request.POST.get('stock_code')
#     code_check = cursor.execute(f'select * from ')
#     stock_name = request.POST.get('stock_name')
#     # 这里搜索成功后就是跳转到展示信息的页面
#     if stock_code:
#         cursor.execute(f'select * from stock_basic_info where SecuCode = {stock_code}')
#         info = cursor.fetchall()
#         data = pd.DataFrameinfo()
#         return HttpResponse("以代码搜索股票")
#     if stock_name:
#         cursor.execute(f'select * from stock_basic_info where SecuCode = {stock_name}')
#         info = cursor.fetchall()
#         data = pd.DataFrameinfo()
#         return HttpResponse("以名字搜索股票")
#     else:
#         return HttpResponse("输入错误")


def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        user_id = request.POST.get("user_id")
        user_password = request.POST.get("user_password")

        check = cursor.execute(f'select * from people where user_id = {user_id}')
        if check:
            return HttpResponse("用户已存在")
        else:
            cursor.execute(f'insert into people(user_id, passwd) values ({user_id},{user_password})')
            # 这里你看看是返回到登录界面还是直接跳到主界面
            return render(request, "home.html")


# 注意体一下，在测试的时候 全局变量type 要设置成为字符串的形式(改int也行)
def delete(request):
    if request.method == "GET":
        if user_type == '2':
            return render(request, 'delete.html')
        else:
            return render(request, 'tmp.html')

    else:
        id = request.POST.get("user_id")
        password = request.POST.get("user_password")

        check = cursor.execute(f'select * from people where user_id = {id} and passwd = {password}')
        if check:
            cursor.execute(f'delete from people where user_id = {id}')
            return render(request, 'delete.html')
        else:
            # 加一个删除失败的跳窗在 delete的界面上
            return HttpResponse("用户或者密码错误")


def stock_basic_info(request):
    if request.method == 'GET':
        return render(request, "stock_basic_info.html")
    else:
        # 获取code和name
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')

        # 以code判断
        if SecuCode:

            check = cursor.execute(f"select * from stock_basic_info where SecuCode = '{SecuCode}'")
            if check:
                global stock_code
                stock_code = SecuCode
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        # 以名字判断
        if Lstknm:

            check = cursor.execute(f"select * from stock_basic_info where  Lstknm = '{Lstknm}'")
            if check:
                global stock_name
                stock_name = Lstknm

                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
            # 什么都没有输入 搜索失败
        else:
            return render(request, "searchFail.html")


def collect(request):
    name = (stock_name or stock_code)
    # print(name)
    cursor.execute(f"insert into collection(user_id, SecuCode) values ('{user_id}','{name}')")
    # print(f"insert into collection(user_id, SecuCode) values ('{user_id}','{name}')")
    return HttpResponse("收藏成功")


def stock_daily_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_daily_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_daily_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_basic_info where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_dividend_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_dividend_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_dividend_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_dividend_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_fees_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_fees_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_fees_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_fees_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_financial_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_financial_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_financial_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_financial_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_price_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_price_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_price_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_price_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_ratios_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_ratios_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_ratios_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_ratios_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_return_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_return_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_return_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_return_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


def stock_shares_data(request):
    if request.method == 'GET':
        if user_type >= 1:
            return render(request, "stock_shares_data.html")
        else:
            return HttpResponse("失败")

    else:
        SecuCode = request.POST.get('SecuCode')
        Lstknm = request.POST.get('Lstknm')
        if SecuCode:
            check = cursor.execute(f"select * from stock_shares_data where SecuCode = '{SecuCode}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)
                print(data)

                return render(request,"show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_shares_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request,"show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")






















def home(request):
    return render(request, 'home.html')


# 展示所有可以搜索的目录
def search_list(request):
    return render(request, "search_list.html")
