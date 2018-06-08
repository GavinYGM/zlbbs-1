import os

# 指定secret_key
SECRET_KEY = os.urandom(24)

DEBUG = True

# 数据库配置信息
HOSTNAME = '118.25.48.34'
PORT = '3306'
DATABASE = 'zlbbs'
USERNAME = 'root'
PASSWORD = '123456'

# PERMANENT_SESSION_LIFETIME = 31 # 设置cookie的保存时间

# DB_URI 连接数据库的配置字符串
DB_URI = 'mysql+pymysql://{username}:{password}@{host}: \
{port}/{db}?charset=utf8'.format(
    username=USERNAME,
    password=PASSWORD,
    host=HOSTNAME,
    port=PORT,
    db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

# 设置跟踪：否，如果设置为true，sqlalchemy中的模型一旦更改，就要发送信号
SQLALCHEMY_TRACK_MODIFICATIONS = False

# 定义一个常量
CMS_USER_ID = 'ASDFSDFASD'
