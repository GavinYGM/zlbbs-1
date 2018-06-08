from flask import session, redirect, url_for
from functools import wraps
import config


# 装饰器1:必须登录
def login_required(func):
    # 用@wraps装饰func，可以保留func的属性
    @wraps(func)
    def inner(*args, **kwargs):
        # 1.判断user
        if config.CMS_USER_ID in session:
            return func(*args, **kwargs)
        else:
            # 重定向到
            return redirect(url_for('cms.login'))

    return inner
