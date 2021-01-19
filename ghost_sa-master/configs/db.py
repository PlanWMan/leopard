# -*- coding: utf-8 -*
# author: unknowwhite@outlook.com
# wechat: Ben_Xiaobai
import pymysql

# 数据库连接

def get_conn_sqldb():
    # 数据库连接程序，支持MySQL 5.7以上和TiDB3
    host = 'localhost'  # 服务器地址
    port = 3306  # 端口号
    user = 'root'  # 用户名
    passwd = '123qwe'
    db = 'ghost_sa'  # 库名
    conn = pymysql.connect(host=host, port=port, user=user,passwd=passwd, db=db, charset='utf8mb4', client_flag=pymysql.constants.CLIENT.MULTI_STATEMENTS)
    return conn