# DjangoStockHub
2023/5/4 启动项目
该项目为了创建一个股票信息查询系统，基于django框架和Python编程语言。
本文件中里面包含了MusicHub 和 dbproject两个参考项目，和StockHub一个最终项目。
stockhub有关的数据库DDL文件，存放在/DjangoTo/StockHub/stockhubtest.sql

数据库的名称请统一设置为：stockhub
数据库的账号请统一设置为：stockhub
数据库的密码请统一设置为: 123456
如下：
    conn = Connection(
        host='localhost',
        port=3306,
        user='stock',
        password='123456',
        autocommit=True
    )
    conn.select_db('stockhub')
    
    
# 参考资料
Git教程：https://bilibili.com/video/av94549514
Github教程：https://www.bilibili.com/video/av98197196/
