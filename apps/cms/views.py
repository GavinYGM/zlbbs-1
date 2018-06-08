from flask import Blueprint, views, g  # 所有模板中都可以访问g对象
from flask import (render_template, request, session, redirect, url_for)
from .forms import LoginForm, ResetPwdForm
from .models import CMSUser
from .decorators import login_required
import config
from exts import db
from utils import restful

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


# @bp.route('/front/')
# def front():
#     return render_template('cms/cms_front.html')


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


# 将类视图`LoginView`注册到路由规则中,并且命名为login，在url_for反转时，填写login
bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

# 将类视图`ResetPwdView`注册到路由规则中,并且命名为login，在url_for反转时，填写resetpwd
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
