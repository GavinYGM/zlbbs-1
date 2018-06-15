from flask import (
    Blueprint,
    views,
    render_template
)

# 蓝图 : 蓝图名字 - __name__ 前台页面的url后面不需要加前缀
bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return 'front index'


class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')
        # return render_template('front/login.html')


bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
