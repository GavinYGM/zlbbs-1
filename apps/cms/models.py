from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class CMSUser(db.Model):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(100), nullable=False)  # 加入_后，变成受保护属性
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, username, password, email):
        self.username = username

        # 这里self.password等于调用下面的password这是密码属性方法，将传进来的password进行加密
        self.password = password

        self.email = email

    # 使用property装饰器：将类中的方法定义成一个属性，虽然是方法， 但是外界再访问这个方法的时候，就和访问属性一模一样
    # 获取密码
    @property
    def password(self):
        '''
            useage:
            user = CMSUser() # 定义对象
            print(user.password) # 访问对象的方法属性
        '''
        return self._password

    # 设置密码：重新定义一个设置方法
    @password.setter
    def password(self, raw_password):
        '''
            useage：
            user.password = 'abc'
        '''
        # 1. 对原生密码进行加密
        self._password = generate_password_hash(raw_password)

    # 检查密码
    def check_password(self, raw_password):
        # self.password -> 访问的还是self._password(经过加密的密码)
        result = check_password_hash(self.password, raw_password)
        return result


# 密码：对外的字段名叫做password
# 密码：对内的字段名叫做_password
