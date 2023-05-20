from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.cache import cache
from django.shortcuts import HttpResponse
from pymysql import Connection
import pandas as pd

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
        userid = request.POST.get("user_id")
        user_password = request.POST.get("user_password")
        if userid and user_password:
            check = cursor.execute(f'select * from people where user_id = {userid}')
            if check:
                warning1 = "The user have already exist!"
                return render(request, "register.html", {"warning1": warning1})
            else:
                cursor.execute(f'insert into people(user_id,user_type, passwd) values ({userid},{2},{user_password})')
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
            return render(request, 'delete.html', {"AllInformation": df})
        else:
            return render(request, 'refuse.html')

    else:
        userid = request.POST.get("user_id")
        password = request.POST.get("user_password")
        if userid and password:
            check = cursor.execute(f'select * from people where user_id = {userid} and passwd = {password}')
            if check:
                cursor.execute(f'delete from people where user_id = {userid}')
                return render(request, 'delete.html')
            else:
                warning1 = "Please input the correct user_id and pass_word"
                return render(request, "delete.html", {"warning1": warning1})
        else:
            warning1 = "Do not leave it empty!"
            return render(request, "delete.html", {"warning1": warning1})


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
                cursor.execute(
                    f"replace into history_record(user_id, record_SecuCode) values ('{user_id}','{SecuCode}')")
                return render(request, "show.html")
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

                return render(request, "show.html")
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


def historysearch(request):
    if request.method == 'GET':
        keyword = request.GET.get('keyword', '')
        if keyword:
            # 将关键字添加到缓存中
            history = cache.get('search_history', [])
            history.append(keyword)
            cache.set('search_history', history, timeout=None)
            # 进行搜索...
            # 返回搜索结果...
    # 获取历史记录列表
    history = cache.get('search_history', [])
    # 渲染模板并返回响应
    return render(request, "historysearch.html")


# myapp/views.py


from django.contrib.auth.decorators import login_required
from .models import UserProfile


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    return render(request, "profile.html")
