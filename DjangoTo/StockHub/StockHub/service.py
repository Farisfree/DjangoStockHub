import string
from pymysql import Connection
from . import views


def changeUSER_TYPE(text):
    views.user_type = text
