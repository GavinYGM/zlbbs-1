from flask import Blueprint

# 蓝图 : 蓝图名字 - __name__ 前台页面的url后面不需要加前缀
bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return 'front index'
