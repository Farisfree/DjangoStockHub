from django.http import HttpResponseRedirect
from django.shortcuts import render
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
user_type = ""
user_id = ""


def login(request):
    warning1 = '（WARNING：Please enter the correct account and password!）'
    if request.method == 'GET':
        return render(request, "login.html")

    else:
        tmp_id = request.POST.get("user_id")
        password = request.POST.get("user_password")

        check = cursor.execute(f"select * from people where user_id = {tmp_id} and passwd = {password}")

        if check:
            info = cursor.fetchall()
            data = pd.DataFrame(info, columns=['user_id', 'user_pwd', 'user_type'])

            global user_id, user_type
            user_id = tmp_id, user_type = data['user_type']
            return render(request, "home.html")
        else:
            return render(request, "login.html", {"warning1": warning1})


# search 这一部分有一点疑问 ： 我们是一个表一个function 还是中间还有一个跳转界面来决定展示哪一部分
# (存疑 回学校跟你说)
def search(request):
    if request.method == 'GET':
        return render(request, "search.html", {"user_type": user_type})

    stock_code = request.POST.get('stock_code')
    stock_name = request.POST.get('stock_name')
    # 这里搜索成功后就是跳转到展示信息的页面
    if stock_code:
        cursor.execute(f'select * from stock_basic_info where SecuCode = {stock_code}')
        info = cursor.fetchall()
        data = pd.DataFrameinfo()
        return HttpResponse("以代码搜索股票")
    if stock_name:
        cursor.execute(f'select * from stock_basic_info where SecuCode = {stock_name}')
        info = cursor.fetchall()
        data = pd.DataFrameinfo()
        return HttpResponse("以名字搜索股票")


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
            return HttpResponse("注册成功")


# 注意体一下，在测试的时候 全局变量type 要设置成为字符串的形式(改int也行)
def delete(request):
    if request.method == "GET":
        if user_type == '2':
            return render(request, 'delete.html')
        else:
            return render(request, 'tmp.html')

    else:
        user_id = request.POST.get("user_id")
        user_password = request.POST.get("user_password")

        check = cursor.execute(f'select * from people where user_id = {user_id} and passwd = {user_password}')
        if check:
            cursor.execute(f'delete from people where user_id = {user_id}')
            return render(request, 'delete.html')
        else:
            # 加一个删除失败的跳窗在 delete的界面上
            return HttpResponse("用户或者密码错误")
