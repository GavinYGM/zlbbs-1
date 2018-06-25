from flask import Blueprint, request
from exts import alidayu
from utils import restful
from utils.captcha import Captcha
from .forms import SMSCaptchaForm

# 蓝图 : 蓝图名字 - __name__ - url前缀
bp = Blueprint("common", __name__, url_prefix='/c')

'''
v1.0 未加密版本发送短信验证码
'''
# @bp.route('/sms_captcha/')
# def sms_captcha():
#     # 传递参数两种方式
#     # 1. ?telephone=xxx
#     # 2. /c/sms_captcha/xxx
#     '''
#     采用第一种传参方式
#     :return:
#     '''
#     # 1. 拿到手机号
#     telephone = request.args.get('telephone')
#     if not telephone:
#         return restful.params_errorr(message='请传入手机号码!')
#
#     # 2. 生成验证码
#     captcha = Captcha.gene_text(number=4)
#
#     # 3. 发送验证码
#     if alidayu.send_sms(telephone=telephone, code=captcha):
#         return restful.success()
#     else:
#         return restful.success()
#         # return restful.params_errorr(message='短信验证码发送失败！')

'''
v1.1 短信验证码加密版本实现
'''


# 传递参数两种方式
# 1. ?telephone=xxx
@bp.route('/sms_captcha/', methods=['POST'])
def sms_captcha():
    '''
    实现：
    1. telephone
    2. timestamp
    3. md5(ts+telephone+salt)
    :return:
    '''
    # 1. 申明验证表单验证对象
    form = SMSCaptchaForm(request.form)
    # 2. 通过验证
    if form.validate():
        # 2.1 拿到手机号
        telephone = form.telephone.data
        # 2.2 生成验证码
        captcha = Captcha.gene_text(number=4)

        # TODO 这里后面要将验证码保存在缓存服务器中
        # print('发送的验证码是：', captcha)

        # 2.3 发送验证码,成功
        if alidayu.send_sms(telephone, code=captcha):

            return restful.success()
        else:
            return restful.params_errorr()
    else:
        return restful.params_errorr(message='参数错误！')
