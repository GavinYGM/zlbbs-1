from flask_script import Manager  # 迁移脚本
from flask_migrate import Migrate, MigrateCommand  # migrate命令
from zlbbs import create_app
from exts import db
from apps.cms import models as cms_models  # 导入的目的：将所有的模型都映射到数据库中

CMSUser = cms_models.CMSUser  # 声明CMSUser模型

app = create_app()

manager = Manager(app)

# 1. 将db和app绑定
Migrate(app, db)

# 2. 将migratecommand添加到manager中，就可以使用db开头的migrate若干命令了
manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('cms用户添加成功！')


if __name__ == '__main__':
    manager.run()
