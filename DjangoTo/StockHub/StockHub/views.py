from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import service
from .models import People
from django.shortcuts import HttpResponse
from pymysql import Connection

conn = Connection(
    host='localhost',
    port=3306,
    user='faris',
    password='123456',
    autocommit=True
)

conn.select_db('stockhub')
cursor = conn.cursor()
user_type = ""


def login(request):
    return render(request, 'login.html', {})


def handleLogin(request):  # This is login page either 在这个function里面会改变两个全局变量
    warning1 = '（WARNING：Please enter the correct account and password!）'
    if request.POST['loginAccount']:
        if request.POST['loginPassword']:
            text1 = request.POST['loginAccount']
            text2 = request.POST['loginPassword']
            db = People.objects.all()
            for i in db:
                if text1 == i.user_id:
                    if text2 == i.passwd:
                        service.changeUSER_TYPE(i.user_type)
                        return HttpResponseRedirect("/home")
    return render(request, 'login.html', {'warning1': warning1})  # 如果说输入栏为空就会报错WARNING


def home(request):  # 这个是home界面
    return HttpResponse("HELLO HOME")
# def test(request):
#     if request.method == 'GET':
#         return render(request, "test.html")
#
#     else:
#         user_id = request.POST.get("user_id")
#         user_password = request.POST.get("user_password")
#
#         check = cursor.execute(f"select * from user_info where user_id = {user_id} and user_pwd = {user_password}")
#
#         info = cursor.fetchall()
#
#         data = pd.DataFrame(info, columns=['user_id', 'user_pwd', 'user_type'])
#
#         user_type = data['user_type']
#
#         if check:
#             return render(request, "tmp.html")
#         else:
#             return HttpResponse("错误")
#
#
# def search(request):
#     if request.method == 'GET':
#         return render(request, "search.html", {"user_type": user_type})
#
#
# def show(request):
#     cursor.execute("select * from user_info")
#     info = cursor.fetchall()
#     print(info)
#
#     data = pd.DataFrame(info, columns=['user_id', 'user_pwd', 'user_type'])
#
#     return render(request, "tmp.html", {"info": info, "data": data})
