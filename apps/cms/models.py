from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 🌟 权限类
class CMSPersmission(object):
    # 255的二进制方式来表示 1111 1111
    # 0. 所有权限
    ALL_PERMISSION = 0b11111111
    # 1. 访问者权限
    VISITOR = 0b00000001
    # 2. 管理帖子权限
    POSTER = 0b00000010
    # 3. 管理评论的权限
    COMMENTER = 0b00000100
    # 4. 管理板块的权限
    BOARDER = 0b00001000
    # 5. 管理前台用户的权限
    FRONTUSER = 0b00010000
    # 6. 管理后台用户的权限
    CMSUSER = 0b00100000
    # 7. 管理后台管理员的权限
    ADMINER = 0b01000000


# 🌟 1. 用户和角色是多对多关系，先定义第三方中间表
cms_role_user = db.Table(
    'cms_role_user',
    db.Column(
        'cms_role_id',
        db.Integer,
        db.ForeignKey('cms_role.id'),
        primary_key=True),
    db.Column(
        'cms_user_id',
        db.Integer,
        db.ForeignKey('cms_user.id'),
        primary_key=True),
)


# 🌟 2. 角色表
class CMSRole(db.Model):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200), nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(
        db.Integer, default=CMSPersmission.VISITOR)  # 默认是访问者权限

    # 将角色表和中间表绑定
    # CMSUser：建立关系的表
    # secodary：中间表
    # backref：反向引用
    users = db.relationship(
        'CMSUser', secondary=cms_role_user, backref='roles')


# 🌟 3. 后台用户
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
