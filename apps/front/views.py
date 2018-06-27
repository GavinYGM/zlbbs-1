from flask import (
    Blueprint,
    views,
    render_template,
    request
)
from .forms import SignupForm
from utils import restful
from .models import FrontUser
from exts import db

# 蓝图 : 蓝图名字 - __name__ 前台页面的url后面不需要加前缀
bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return 'front index'


'''
    测试验证码功能
'''


# @bp.route('/sms_captcha/')
# def sms_captcha():
#     result = alidayu.send_sms(telephone='15927678712', code='我是不语你是胡巴')
#     if result:
#         return '发送成功!'
#     else:
#         return '发送失败!'


# 🌟 Front：注册类视图
class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')
        # return render_template('front/login.html')

    # 注册流程
    def post(self):
        form = SignupForm(request.form)
        # 通过验证
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            user = FrontUser(telephone=telephone, username=username, password=password)
            db.session.add(user)
            db.session.commit()
            return restful.success()
        # 未通过验证
        else:
            # 打印错误
            print('未通过验证，错误信息：', form.get_error())
            # 返回错误信息
            return restful.params_error(message=form.get_error())


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
