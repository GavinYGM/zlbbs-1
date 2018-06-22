from flask import Blueprint, request
from exts import alidayu
from utils import restful
from utils.captcha import Captcha

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

'''
@bp.route('/sms_captcha/')
def sms_captcha():
    # 传递参数两种方式
    # 1. ?telephone=xxx
    # 2. /c/sms_captcha/xxx
    '''
    采用第一种传参方式
    :return:
    '''
    # 1. 拿到手机号
    telephone = request.args.get('telephone')
    if not telephone:
        return restful.params_errorr(message='请传入手机号码!')

    # 2. 生成验证码
    captcha = Captcha.gene_text(number=4)

    # 3. 发送验证码
    if alidayu.send_sms(telephone=telephone, code=captcha):
        return restful.success()
    else:
        return restful.success()
        # return restful.params_errorr(message='短信验证码发送失败！')
