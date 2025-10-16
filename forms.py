from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

# 创建一个继承自 FlaskForm 的类
class ContactForm(FlaskForm):
    # 定义表单的字段
    # 第一个参数是字段的 label (标签)
    # validators 是一个验证器列表
    name = StringField('你的名字', validators=[DataRequired(message="名字不能为空。")])

    email = StringField('你的邮箱', validators=[
        DataRequired(message="邮箱不能为空。"),
        Email(message="请输入有效的邮箱地址。")
    ])

    message = TextAreaField('消息内容', validators=[DataRequired(message="消息内容不能为空。")])

    submit = SubmitField('提交')