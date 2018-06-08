from flask import jsonify


# http状态码 - 转code码
class HttpCode(object):
    ok = 200
    unautherror = 401
    paramerror = 400
    servererror = 500


# 对jsonify进行封装，传入code，message，data
def restful_result(code, message, data):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return jsonify({'code': code, 'message': message, 'data': data or {}})


def success(message=None, data=None):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.ok, message=message, data=data)


def unauth_error(message=''):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(
        code=HttpCode.unautherror, message=message, data=None)


def params_errorr(message=''):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(code=HttpCode.paramerror, message=message, data=None)


def server_error(message=''):
    '''
    :param code: 状态码
    :param message: 返回错误信息
    :param data: 返回数据
    '''
    return restful_result(
        code=HttpCode.servererror, message=message or '服务器内部错误', data=None)
