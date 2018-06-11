from flask import Blueprint, views, g  # 所有模板中都可以访问g对象
from flask import (render_template, request, session, redirect, url_for)
from .forms import LoginForm, ResetPwdForm, ResetEmailForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db, mail
from flask_mail import Message  # 导入Message类
from utils import restful, zlcache
import string
import random
# 蓝图 (全局的): 蓝图名字 - __name__ - url前缀
bp = Blueprint("cms", __name__, url_prefix='/cms')


# 🌟 cms后台管理系统的首页
@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


# 🌟 cms后台管理系统的注销
@bp.route('/logout/')
@login_required
def logout():
    # 方式一：清空session:略显暴力
    # session.clear()

    # 方式二：删除session中的config.CMS_USER_ID
    del session[config.CMS_USER_ID]
    return redirect(url_for('cms.login'))


# 🌟 cms后台管理系统的个人信息
@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


# 🌟 cms后台管理系统的修改邮箱获取验证码
@bp.route('/email_captcha/')
@login_required
def email_captcha():
    # 0. 邮箱验证:正则校验
    # 通过验证：
    email = request.args.get('email')
    import re
    if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}| \
            [0-9]{1,3})(\\]?)$", email) is not None:
        # /email_capicha/?email=xxx@qq.com - 通过查询字符串的形式将邮箱传递到后台
        # 1. 查询字符串
        email = request.args.get('email')
        if not email:
            return restful.params_errorr('请传递邮箱参数！')

        # 2. 产生验证码
        # 2.1 a-zA-Z的字符串
        source = list(string.ascii_letters)

        # 2.2 将一个列表的值更新到另一个列表中，利用list.extend()
        # 方法1
        # source.extend(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])

        # 方法2
        # map(func,obj) 将obj(需要可迭代的对象)的数据传递到函数中，然后处理后再返回
        # lambda函数：匿名函数
        # lambda x:str(x) 定义一个匿名函数，变量为x,处理方式为将x传入到str()中，进行字符串转义
        source.extend(map(lambda x: str(x), (range(0, 10))))

        # 2.3 随机采样
        # sample 采样器，从source中随机选择6个，返回值为列表
        list_captcha = random.sample(source, 6)

        # 将字符串转换成列表
        captcha = "".join(list_captcha)

        # 3.给这个邮箱发送邮件
        message = Message(
            '武汉柠檬班论坛邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
        try:
            mail.send(message)
        except Exception as e:
            return restful.server_error()
        # 4. 存验证码,key=email,value=captcha
        zlcache.set(email, captcha)

        return restful.success()
    else:
        return restful.params_errorr(message='请输入正确的邮箱格式！')


# '''
#     测试邮箱发送邮件
# '''

# @bp.route('/email/')
# def send_email():
#     message = Message('邮件发送', recipients=['1668319858@qq.com'], body='测试')
#     mail.send(message)
#     return '邮件发送成功！'


# 🌟 类视图:登录类视图
class LoginView(views.MethodView):
    def get(self, message=None):
        # 🌟 cms后台管理系统登录页
        return render_template('cms/cms_login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            # 1. 先通过email的唯一性查询到CMSUser表中的user对象
            user = CMSUser.query.filter_by(email=email).first()

            # 2. 验证密码：如果user存在，并且检查了密码之后
            if user and user.check_password(password):
                # 保存用户登录信息，保存在session中，session是用字典存取CMS_USER_ID
                session[config.CMS_USER_ID] = user.id
                # 如果用户点了记住我
                if remember:
                    # 如果设置session.permanent = True
                    # 那么过期时间是31天
                    # session持久化，默认是31天
                    session.permanent = True
                # ⚠️ 这里url_for()进行反转的时候，必须先写：蓝图名.index
                # 🌟 跳转到cms后台管理首页
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误!')
        else:
            # 返回 ('password',['请输入正确格式的密码']) [1][0]
            message = form.errors.popitem()[1][
                0]  # forms.errors.popitem返回字典的任意一项
            return self.get(message=message)


# 🌟 修改密码类视图
class ResetPwdView(views.MethodView):
    # 在类视图中调用装饰器
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetPwdForm(request.form)
        # 表单验证通过
        if form.validate():
            # 1. 拿到oldpwd
            oldpwd = form.oldpwd.data
            # 2. 拿到newpwd
            newpwd = form.newpwd.data
            # 从`g`对象上先拿到user
            user = g.cms_user
            # 验证密码：
            if user.check_password(oldpwd):
                # 验证成功之后，将新密码设置到user.passwrod中
                user.password = newpwd
                db.session.commit()
                # 因为请求是通过ajax发送过来的，所以返回给前端的数据也要用json数据来返回
                '''
                返回的格式一般采用：
                    :params code: 代表状态返回码
                    :params mssage: 代表返回信息
                Example usage::
                    {'code' : 200 , 'message' : 'xxxxx'}
                '''
                # return jsonify({'code': 200, 'message': '密码修改成功'})
                return restful.success()
            else:
                # return jsonify({'code': 400, 'message': '旧密码错误！'})
                return restful.params_errorr(message='旧密码错误！')
        else:
            # 获取错误信息
            # message = form.get_error()
            # return message
            return restful.params_errorr(message=form.get_error())


# 🌟 重设邮箱视图类
class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        # 1. 验证表单
        if form.validate():
            email = form.email.data
            g.cms_user.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_errorr(form.get_error())


# 将类视图`LoginView`注册到路由规则中,并且命名为login，在url_for反转时，填写login
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

# 将类视图`ResetPwdView`注册到路由规则中,并且命名为login，在url_for反转时，填写resetpwd
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))

bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
