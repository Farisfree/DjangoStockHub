import string
from pymysql import Connection
from .models import Searchresult, UsersTable
from . import views

conn = Connection(
    host='localhost',
    port=3306,
    user='root',
    password='root',
    autocommit=True
)
conn.select_db('music')
cursor = conn.cursor()


def addSearch(text):  # 在数据库的search result表中添加新的搜索内容（目前无用）
    search1 = Searchresult(searchinformation=text)
    search1.save()


def addUser(text):  # 在数据库的users_table里面添加新的用户（注册界面），只可以注册普通用户
    user1 = UsersTable(id=text[0], password1=text[1], usertype=0)
    user1.save()


def addAnyUser(text):  # 在数据库的users_table里面添加新的用户，可以注册普通用户和管理员用户
    user1 = UsersTable(id=text[0], password1=text[1], usertype=text[2])
    user1.save()


def change_currLogin(text):  # 改变全局变量 currLogin
    db = UsersTable.objects.all()
    for i in db:
        if text == i.id:
            views.currLogin = i.usertype


def change_deleteUserTable(text):  # 改变全局变量 deleteUserTable
    views.deleteUserTable = text


def deleteUser(text):  # 从数据库的users_table中删除用户
    UsersTable.objects.get(id=text).delete()


def checkPasswd(str_in):  # 检查密码是否是 7-11 位并且只包含大小写字母或者数字
    pwd_list = str_in
    pwd_range1 = string.ascii_letters
    pwd_range2 = string.digits

    if len(pwd_list) < 6 or len(pwd_list) > 12:
        return False

    for i in pwd_list:
        if i not in pwd_range1 + pwd_range2:
            return False
        else:
            return True


def checkId(str_in):  # 检查账号是否只包含大小写字母和数字
    id_list = str_in

    id_range1 = string.ascii_letters
    id_range2 = string.digits

    for i in id_list:
        if i not in id_range1 + id_range2:
            return False
        else:
            return True


def checkType(str_in):  # 检测输入的数据类型是否仅为0或者1
    type_list = str_in
    if type_list in ['0', '1']:
        return True
    else:
        return False


def showSong():  # 返回搜索量最高的五个歌曲，并且以二维数组的方式返回他们的相关信息
    cursor.execute(
        "select SongData.title,SongData.artist,SongData.album,SongData.times from song_data SongData order by "
        "SongData.search_time desc limit 0,5")
    songData = cursor.fetchall()
    return songData


def updateSearch(song):  # 改变数据库中song_data表的search_time列
    result = song
    cursor.execute("update song_data set search_time = (search_time + 1) where title like '%" + result + "%'")


def changeCurrAccount(text):  # 改变全局变量currAccount
    views.currAccount = text
