from django.shortcuts import render, HttpResponse
import pandas as pd
# Create your views here.
from pymysql import Connection

conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='wu101402',
    autocommit=True
)

conn.select_db('database_project')
cursor = conn.cursor()

user_type = ""


def test(request):
    if request.method == 'GET':
        return render(request, "test.html")

    else:
        user_id = request.POST.get("user_id")
        user_password = request.POST.get("user_password")

        check = cursor.execute(f"select * from user_info where user_id = {user_id} and user_pwd = {user_password}")

        info = cursor.fetchall()

        data = pd.DataFrame(info, columns=['user_id', 'user_pwd', 'user_type'])

        user_type = data['user_type']

        if check:
            return render(request, "refuse.html")
        else:
            return HttpResponse("错误")


def search(request):
    if request.method == 'GET':
        return render(request, "search.html", {"user_type": user_type})


def show(request):
    cursor.execute("select * from user_info")
    info = cursor.fetchall()
    print(info)

    data = pd.DataFrame(info, columns=['user_id', 'user_pwd', 'user_type'])

    return render(request, "refuse.html", {"info": info, "data": data})
