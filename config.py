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

# 定义一个常量:用来存cms模块的用户id
CMS_USER_ID = 'ASDFSDFASD'

# flask-email
# 🌟 发送者邮箱的服务器地址
# ⚠️ QQ邮箱不支持非加密方式发送邮件
MAIL_SERVER = "smtp.qq.com"
MAIL_PORT = "587"
MAIL_USE_TLS = True  # 如果使用TLS加密协议，使用端口号：587
# MAIL_USE_SSL = False # 如果使用SSL加密协议，使用端口号：465
# MAIL_DEBUG = 默认为 app.debug # 默认是根据app上的debug来打印日志
MAIL_USERNAME = "291008572@qq.com"  # QQ邮箱
MAIL_PASSWORD = "brlrqdotgkcicbbh"  # 授权码
MAIL_DEFAULT_SENDER = "291008572@qq.com"  # 默认发送者
