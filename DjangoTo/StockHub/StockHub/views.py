import pandas as pd
from django.shortcuts import HttpResponse
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
user_type = 2  # 用来判断用户类型
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

                tmp_type = int(info[0][0])
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

                cursor.execute(
                    f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{SecuCode}')")
                return render(request, "show.html", {'data': info})
            else:
                return render(request, "searchFail.html")
        # 以名字判断
        if Lstknm:

            check = cursor.execute(f"select * from stock_basic_info where  Lstknm = '{Lstknm}'")
            if check:
                global stock_name
                stock_name = Lstknm

                info = cursor.fetchall()

                return render(request, "show.html", {'data': info})
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


def collectInterface(request):
    cursor.execute("Select * from collection")
    info = cursor.fetchall()
    return render(request, "collectInterface.html", {'data': info})


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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select stock_daily_data.* from stock_daily_data \
                                        join (select distinct stock_basic_info.SecuCode from stock_basic_info\
                                         where Lstknm ='{Lstknm}') as tmp using(SecuCode) \
                                          where tmp.SecuCode = stock_daily_data.Secucode")

            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_dividend_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_fees_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_financial_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_price_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_ratios_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_return_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

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

                return render(request, "show.html")
            else:
                return render(request, "searchFail.html")
        if Lstknm:
            check = cursor.execute(f"select * from stock_shares_data where  Lstknm = '{Lstknm}'")
            if check:
                info = cursor.fetchall()
                data = pd.DataFrame(info)

                return render(request, "show.html")

            else:
                return render(request, "searchFail.html")

        else:
            return render(request, "searchFail.html")


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
