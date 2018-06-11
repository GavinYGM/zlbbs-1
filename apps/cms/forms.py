from wtforms import StringField, IntegerField
from wtforms.validators import Email, InputRequired, Length, EqualTo
from ..forms import BaseForm


# 写表单验证器
class LoginForm(BaseForm):
    email = StringField(validators=[
        Email(message='请输入正确的邮箱格式'),
        InputRequired(message='请输入邮箱')
    ])

    password = StringField(validators=[
        Length(6, 20, message='请输入正确格式的密码'),
        InputRequired(message='请输入密码')
    ])

    remember = IntegerField()


# 重设密码验证器
class ResetPwdForm(BaseForm):
    oldpwd = StringField(validators=[
        Length(6, 20, message='请输入正确格式的新密码'),
    ])

    newpwd = StringField(validators=[
        Length(6, 20, message='请输入正确格式的旧密码'),
    ])

    newpwd2 = StringField(
        validators=[EqualTo("newpwd", message='确认密码必须和新的密码保持一致')])


# 修改邮箱验证器
class ResetEmailForm(BaseForm):
    email = StringField(validators=[
        Email(message='请输入正确的邮箱格式'),
        InputRequired(message='请输入邮箱')
    ])
