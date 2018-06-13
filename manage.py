from flask_script import Manager  # 迁移脚本
from flask_migrate import Migrate, MigrateCommand  # migrate命令
from zlbbs import create_app
from exts import db
from apps.cms import models as cms_models  # 导入的目的：将所有的模型都映射到数据库中

CMSUser = cms_models.CMSUser  # 声明CMSUser模型
CMSRole = cms_models.CMSRole
CMSPermission = cms_models.CMSPersmission

app = create_app()

manager = Manager(app)

# 1. 将db和app绑定
Migrate(app, db)

# 2. 将migratecommand添加到manager中，就可以使用db开头的migrate若干命令了
manager.add_command('db', MigrateCommand)


# 🌟 利用flask-script :新建后台管理用户
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')


# 🌟 创建角色
@manager.command
def create_role():
    # 1. 访问者
    vistor = CMSRole(name='访问者', desc='只能访问相关数据，不能修改。')
    vistor.permissions = CMSPermission.VISITOR

    # 2. 运营角色(修改个人信息，管理帖子，管理评论，管理前台用户)
    operator = CMSRole(name='运营', desc='管理帖子，管理评论，管理前台用户。')
    operator.permissions = CMSPermission.VISITOR |  \
        CMSPermission.POSTER | CMSPermission.FRONTUSER | \
        CMSPermission.COMMENTER | CMSPermission.CMSUSER

    # 3. 管理员(拥有绝大部分权限)
    admin = CMSRole(name='管理员', desc='拥有本系统所有权限。')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | \
        CMSPermission.CMSUSER | CMSPermission.COMMENTER | \
        CMSPermission.FRONTUSER | CMSPermission.BOARDER

    # 4. 开发者(拥有网站所有权限)
    developer = CMSRole(name='开发者', desc='开发人员专用角色。')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([vistor, operator, admin, developer])
    db.session.commit()


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    # 1. 通过email查询用户
    user = CMSUser.query.filter_by(email=email).first()
    # 2. 如果用户存在
    if user:
        # 3. 通过name查询角色
        role = CMSRole.query.filter_by(name=name).first()
        # 4. 如果角色存在
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色成功！')
        else:
            print('没有这个角色：%s' % name)


# 测试用户是否拥有某种权限
@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('这个用户有访问者的权限！')
    else:
        print('这个用户没有访问者的权限！')


if __name__ == '__main__':
    manager.run()
