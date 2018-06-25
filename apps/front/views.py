from flask import (
    Blueprint,
    views,
    render_template,
    make_response
)
from utils.captcha import Captcha
from io import BytesIO
from exts import alidayu

# 蓝图 : 蓝图名字 - __name__ 前台页面的url后面不需要加前缀
bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return 'front index'


# 🌟 Front：获取图像验证码视图
@bp.route('/captcha/')
def graph_captcha():
    # 获取验证码
    text, image = Captcha.gene_graph_captcha()
    # BytesIO:字节流 - out:声明二进制流对象
    out = BytesIO()
    # 将图片保存到image对象，指定图片格式png
    image.save(out, 'png')
    # 将指针指定在0位置
    out.seek(0)
    # 读取并返回
    resp = make_response(out.read())
    # 指定类型
    resp.content_type = 'image/png'
    # 返回图片
    return resp

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


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
