from flask import Blueprint

# 蓝图 : 蓝图名字 - __name__ - url前缀
bp = Blueprint("common", __name__, url_prefix='/common')


@bp.route('/')
def index():
    return 'common index'
