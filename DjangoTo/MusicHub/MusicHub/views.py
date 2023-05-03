import random

import matplotlib.pyplot as plt
import pandas as pd
import pylab as pl
from django.http import HttpResponseRedirect
from django.shortcuts import render
from . import service
from .models import SongData, UsersTable

currAccount = ""  # The account number of the current user
currLogin = ""  # The user type of the current user
deleteUserTable = [[]]


def login(request):  # This is login page
    return render(request, 'login.html', {})


def handleLogin(request):  # This is login page either 在这个function里面会改变两个全局变量
    warning1 = '（WARNING：Please enter the correct account and password!）'
    if request.POST['loginAccount']:
        if request.POST['loginPassword']:
            text1 = request.POST['loginAccount']
            text2 = request.POST['loginPassword']
            service.change_currLogin(text1)
            service.changeCurrAccount(text1)
            db = UsersTable.objects.all()
            for i in db:
                if text1 == i.id:
                    if text2 == i.password1:
                        return HttpResponseRedirect("/home")
    return render(request, 'login.html', {'warning1': warning1})  # 如果说输入栏为空就会报错WARNING


def search(request):  # 这个是search的界面
    return render(request, "search.html", {})


def handle(request):  # 这个是search界面，在这个界面分为三种情况，第一个情况是只输入歌曲名，第二个情况是只输入作者名，第三个情况是同时输入作者名和歌曲名。
    po_list = []
    counter = 0
    if request.POST['根据歌曲搜索']:
        if request.POST['根据作者搜索']:
            text1 = request.POST['根据歌曲搜索']
            text2 = request.POST['根据作者搜索']
            #            service.addSearch(text1)
            service.updateSearch(text1)  # 把搜索的歌曲输入到数据库的 search result 表里（目前无用）
            db = SongData.objects.all()
            row = []
            po_list = []
            for i in db:
                if (text1 in i.title) and (text2 in i.artist):
                    row.append(i.id)
                    row.append(i.title)
                    row.append(i.artist)
                    row.append(i.album)
                    row.append(i.times)
                    po_list.append(row)
                    counter = counter + 1
                    row = []
        else:
            text = request.POST['根据歌曲搜索']
            # service.addSearch(text)
            service.updateSearch(text)
            db = SongData.objects.all()
            row = []
            po_list = []
            for i in db:
                if text in i.title:
                    row.append(i.id)
                    row.append(i.title)
                    row.append(i.artist)
                    row.append(i.album)
                    row.append(i.times)
                    po_list.append(row)
                    counter = counter + 1
                    row = []
    elif request.POST['根据作者搜索']:
        text = request.POST['根据作者搜索']
        service.addSearch(text)
        db = SongData.objects.all()
        row = []
        po_list = []
        for i in db:
            if text in i.artist:
                row.append(i.id)
                row.append(i.title)
                row.append(i.artist)
                row.append(i.album)
                row.append(i.times)
                po_list.append(row)
                counter = counter + 1
                row = []

    if len(po_list) == 0:
        warnings = 'No search results, please re-enter the search content'  # 如果没有搜索结果就会返回这个warning
        return render(request, "search.html", {"warnings": warnings})

    if counter == 1:
        return render(request, "resp.html", {"resp": po_list, "counter": counter})  # resp.html 是搜索的结果界面
    else:
        return render(request, "resp2.html", {"resp": po_list, "counter": counter})  # resp.html 是搜索的结果界面


def handleRegistration(request):  # 这个是registration界面，这里会验证你输入的账号和密码是否合法，如果不合法就会弹出相应的提示
    warning = "It couldn't be empty!"
    if request.POST['AccountNumber']:
        if request.POST['Password']:
            if service.checkId(request.POST['AccountNumber']):  # 调用checkID函数检测账号合法性
                if service.checkPasswd(request.POST['Password']):  # 调用checkPasswd函数检测密码合法性
                    counter = 0
                    ac = UsersTable.objects.all()
                    for i in ac:
                        if request.POST["AccountNumber"] == i.id:
                            counter = 1
                    if counter == 0:
                        accountnumber = request.POST['AccountNumber']
                        password = request.POST['Password']
                        text = [accountnumber, password]
                        hint = "You have successfully registered"
                        service.addUser(text)
                        return render(request, 'login.html', {"hint": hint})
                    else:
                        hint = "This user has already registered"
                        return render(request, 'login.html', {"hint": hint})  # 检测数据库中是否已经存在该账号
                else:
                    warning = "Please input a password with length of 7-11 which only contains letters and digits."
                    return render(request, 'registration.html', {'warning': warning})  # 检测输入的密码是否合法
            else:
                warning = "Please input a account which only contains letters and digits."
                return render(request, 'registration.html', {'warning': warning})  # 检测输入的账号是否合法
    else:
        return render(request, 'registration.html', {'warning': warning})  # 输入栏如果为空就会提示warning


def registration(request):  # 这个是registration界面
    return render(request, "registration.html", {})


def home(request):  # 这个是home界面
    rand = random.sample(range(1, 40000), 5)
    db = SongData.objects.all()
    row = []
    po_list = []
    for i in db:
        for randNum in rand:
            if int(randNum) == i.id:
                row.append(i.title)
                row.append(i.artist)
                row.append(i.album)
                po_list.append(row)
                row = []
    recommendsongtable = service.showSong()
    return render(request, 'home.html',
                  {'hottestsongtable': po_list, 'recommandsongtable': recommendsongtable})


def personalCenter(request):  # 这个是personalCenter界面
    db = UsersTable.objects.all()
    personalcentertable = []
    personalcentertable1 = []
    for i in db:
        if i.id == currAccount:
            strid = i.id
            personalcentertable.append(strid)
            if i.usertype == 0:
                text = "Normal User"
                personalcentertable.append(text)
            else:
                text = "Administrator"
                personalcentertable.append(text)
            personalcentertable1 = [personalcentertable]
    return render(request, 'personalCenter.html', {'personalcentertable': personalcentertable1})


def userInformation(request):  # 这个是（管理员）userInformation界面
    personalise = []
    usertable = []
    if currLogin == 0:
        return render(request, 'userInformation_normalUser.html')
    else:
        db = UsersTable.objects.all()
        for i in db:
            personalise.append(i.id)
            if i.usertype == 0:
                text1 = "Normal User"
                personalise.append(text1)
            else:
                text1 = "Administrator"
                personalise.append(text1)
            usertable.append(personalise)
            personalise = []
            service.change_deleteUserTable(usertable)
        return render(request, 'userInformation.html', {'userinformationtable': usertable})


def userInformation_normalUser(request):  # 这个是（普通用户）userInformation的界面
    return render(request, 'userInformation_normalUser.html')


def deleteUser(request):  # 这个是从 userInformation界面转入 删除成功界面
    text = request.POST["删除的用户"]
    service.deleteUser(text)  # 执行删除函数
    return render(request, 'successfulDelete.html')


def addAnyUser(request):  # 这个是从 userInformation界面转入 添加成功界面 或者转入 添加失败界面
    if (request.POST['AccountNumber']) and (request.POST['Password']) and (request.POST['UserType']):
        text = [request.POST['AccountNumber'], request.POST['Password'], request.POST['UserType']]
        if service.checkType(request.POST['UserType']):  # 检测输入的用户类型是否合法
            if service.checkId(request.POST['AccountNumber']):  # 检测输入的账号是否合法
                if service.checkPasswd(request.POST['Password']):  # 检测输入的密码是否合法
                    counter = 0
                    ac = UsersTable.objects.all()
                    for i in ac:
                        if request.POST["AccountNumber"] == i.id:
                            counter = 1
                    if counter == 0:
                        service.addAnyUser(text)
                        return render(request, 'successfulAdd.html')
                    else:
                        return render(request, 'alreadyAdd.html')
                else:
                    return render(request, 'illegal.html')
            else:
                return render(request, 'illegal.html')
        else:
            return render(request, 'illegal.html')
    return render(request, 'userInformation_normalUser.html')


def dataAnalysis(request):
    table1 = [[]]  # 歌曲的数量 和 作者
    dict1 = dict()
    table2 = [[]]  # 歌曲的数量 和 album
    dict2 = dict()
    table3 = [[]]  # 歌曲的数量 和 时长
    db = SongData.objects.all()

    for i in db:
        if i.artist in dict1.keys():
            dict1[i.artist] = dict1[i.artist] + 1
        else:
            dict1[i.artist] = 1
    for i in dict1.keys():
        row = [i, dict1[i]]
        table1.append(row)
    table1 = table1[1:]
    sum1 = 0
    counter1 = 0
    for i in table1:
        sum1 = sum1 + i[1]
        counter1 = counter1 + 1

    average1 = sum1 / counter1
    dataframe1 = pd.DataFrame(table1, columns=["Artist", "Number"])
    dataframe1.set_index(["Artist"], inplace=True)
    dataframe1.sort_values("Number", inplace=True, ascending=False)
    maxinum1 = dataframe1["Number"].max()
    mininum1 = dataframe1["Number"].min()
    ##  用这些代码生成前20作者的歌曲数量图
    # pl.rcParams['font.sans-serif'] = ['SimHei']
    # pl.rcParams['axes.unicode_minus'] = False
    # dataframe1 = dataframe1[0:20]
    # plt.figure()
    # dataframe1.plot.barh(alpha=0.5)
    # plt.savefig("1.png")
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    for i in db:
        if i.album in dict2.keys():
            dict2[i.album] = dict2[i.album] + 1
        else:
            dict2[i.album] = 1
    for i in dict2.keys():
        row = [i, dict2[i]]
        table2.append(row)
    table2 = table2[1:]
    sum2 = 0
    counter2 = 0
    for i in table2:
        sum2 = sum2 + i[1]
        counter2 = counter2 + 1
    average2 = sum2 / counter2
    dataframe2 = pd.DataFrame(table2, columns=["Album", "Number"])
    dataframe2.set_index(["Album"], inplace=True)
    dataframe2.sort_values("Number", inplace=True, ascending=False)
    maxinum2 = dataframe2["Number"].max()
    mininum2 = dataframe2["Number"].min()
    ##  用这些代码生成前20歌单的歌曲数量图
    # pl.rcParams['font.sans-serif'] = ['SimHei']
    # pl.rcParams['axes.unicode_minus'] = False
    # dataframe2 = dataframe2[0:20]
    # plt.figure()
    # dataframe2.plot.barh(alpha=0.5)
    # plt.savefig("2.png")
    return render(request, 'dataAnalysis.html',
                  {"average1": average1, "average2": average2, "maxinum1": maxinum1, "maxinum2": maxinum2,
                   "mininum1": mininum1, "mininum2": mininum2, "counter2":counter2, "counter1":counter1})
