#!/usr/bin/python
#-*- coding: UTF-8 -*-
from __future__ import unicode_literals
from flask_wtf import FlaskForm
from wtforms import RadioField, SubmitField, StringField,IntegerField,PasswordField,SelectField
from wtforms.validators import DataRequired, Length,NumberRange

class TodoListForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    status = RadioField('是否完成', validators=[DataRequired()],  choices=[("1", '是'),("0",'否')])
    submit = SubmitField('ADD')
class PublishForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(1, 64)])
    class_name = StringField('课程', validators=[DataRequired(),  Length(1,64)])
    submit = SubmitField('发布')
class ClassForm(FlaskForm):
    class_name = StringField('课程', validators=[DataRequired(),  Length(1,64)])
    class_teacher = StringField('老师', validators=[DataRequired(),  Length(1,64)])
    class_place = StringField('地点', validators=[DataRequired(),  Length(1,64)])
    class_whichweek = StringField('在哪几周上课', validators=[DataRequired(),Length(1,64) ])
    class_order = IntegerField('第几节',validators=[DataRequired(),NumberRange(1,4)])
    class_weekday = IntegerField('星期几',validators=[DataRequired(),NumberRange(1,7)])
    submit = SubmitField('添加')
class NewClassForm(FlaskForm):
    class_name = StringField('课程', validators=[DataRequired(),  Length(1,64)])
    class_teacher = StringField('老师', validators=[DataRequired(),  Length(1,64)])
    class_place = StringField('地点', validators=[DataRequired(),  Length(1,64)])
    class_weekbeg=IntegerField('第几周开始',validators=[DataRequired(),NumberRange(1,20)])
    class_weekend = IntegerField('第几周结束', validators=[DataRequired(), NumberRange(1, 20)])
    class_weekparity=SelectField("单双周",choices=[('0','单周'), ('1',"双周"),('2',"全周")])
    class_order = IntegerField('第几节',validators=[DataRequired(),NumberRange(1,4)])
    class_weekday = IntegerField('星期几',validators=[DataRequired(),NumberRange(1,7)])
    submit = SubmitField('添加')
class AdminForm(FlaskForm):
    user_id = StringField('学号/工号', validators=[DataRequired(),  Length(1,64)])
    user_name = StringField('名字', validators=[DataRequired(),  Length(1,64)])
    user_type = RadioField('老师/学生', validators=[DataRequired()],  choices=[("teacher", '老师'),("student",'学生')])
    submit = SubmitField('添加')
class ResetPasswordForm(FlaskForm):
    user_id=StringField('学号/工号', validators=[DataRequired(),  Length(1,64)])
    user_password=PasswordField('旧密码', validators=[DataRequired(),  Length(1,64)])
    user_newpassword=PasswordField('新密码', validators=[DataRequired(),  Length(1,64)])
    submit = SubmitField('重置')
