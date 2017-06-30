#!/usr/bin/python
# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

import time

import pymysql
from flask import (Flask, render_template, g, session, redirect, url_for,
                   request, flash, abort)
from flask_bootstrap import Bootstrap
from flask_script import Manager
from forms import TodoListForm, PublishForm, ClassForm, AdminForm, ResetPasswordForm, NewClassForm

SECRET_KEY = 'This is my key'

app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)

app.secret_key = SECRET_KEY
app.config['USERNAME'] = 'admin'
app.config['PASSWORD'] = 'admin'


def connect_db():
    """Returns a new connection to the database."""
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='123',
                           db='class_table',
                           charset='utf8')


def current_week():
    return 1


@app.before_request
def before_request():
    """Make sure we are connected to the database each request."""
    g.db = connect_db()


@app.after_request
def after_request(response):
    """Closes the database again at the end of the request."""
    g.db.close()
    return response




@app.route('/', methods=['GET', 'POST'])
def show_todo_list():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    form = TodoListForm()
    if request.method == 'GET':
        if (session["type"] == "student"):
            publishes = []
            with g.db as cur:
                sql3 = "select title,class_name from publishes"
                cur.execute(sql3)
                publishes = [dict(title=row[0], class_name=row[1]) for row in cur.fetchall()]

            for publish in publishes:
                with g.db as cur:
                    sql4 = "select distinct user_id,class_name from class_table where user_id='{0}'".format(
                        session["id"])
                    cur.execute(sql4)
                    students = [dict(user_id=row[0], class_name=row[1]) for row in cur.fetchall()]
                    for student in students:
                        if student["class_name"] == publish["class_name"]:
                            flash(publish["class_name"] + "的课程通知:" + publish["title"])

        sql = 'select id,class_order, class_weekday, class_name, class_teacher, class_place ,class_weekbeg,class_weekend,class_weekparity ' \
              'from class_table where user_id="{0}"'.format(session["id"])
        with g.db as cur:
            cur.execute(sql)
            classtable = [dict(id=int(row[0]), class_order=int(row[1]), class_weekday=int(row[2]), class_name=row[3],
                               class_teacher=row[4],
                               class_place=row[5], class_weekbeg=int(row[6]), class_weekend=int(row[7]),
                               class_weekparity=int(row[8])) for row in cur.fetchall()]

            ctable = [[""] * 7 for i in range(4)]

            for i in range(3):
                for j in range(7):
                    ctable[i].append("")
            if request.args.get("whichweek"):
                whichweek=int(request.args.get("whichweek"))
            else:
                whichweek=current_week()
            for c in classtable:
                if c["class_weekparity"] == 2:
                    if c["class_weekbeg"] <= whichweek and c["class_weekend"] >= whichweek:
                        ctable[c["class_order"] - 1][c["class_weekday"] - 1] = c["class_name"] + "|" + c[
                            "class_teacher"] + "|" + c["class_place"]
                if c["class_weekparity"] == 1 and whichweek % 2 == 0:
                    if c["class_weekbeg"] <= whichweek and c["class_weekend"] >= whichweek:
                        ctable[c["class_order"] - 1][c["class_weekday"] - 1] = c["class_name"] + "|" + c[
                            "class_teacher"] + "|" + c["class_place"]
                if c["class_weekparity"] == 0 and whichweek % 2 == 1:
                    if c["class_weekbeg"] <= whichweek and c["class_weekend"] >= whichweek:
                        ctable[c["class_order"] - 1][c["class_weekday"] - 1] = c["class_name"] + "|" + c[
                            "class_teacher"] + "|" + c["class_place"]
        sql2 = 'select id, user_id, title, status, create_time from todolist where user_id="{0}"'.format(session["id"])
        with g.db as cur:
            cur.execute(sql2)
            todo_list = [dict(id=row[0], user_id=row[1], title=row[2], status=bool(row[3]),
                              create_time=time.asctime(time.localtime(int(row[4])))) for row
                         in cur.fetchall()]
        return render_template('index.html', ctable=ctable, form=form, todo_list=todo_list,whichweek=whichweek,current_week=current_week())
    else:
        if form.validate_on_submit():
            title = form.title.data
            status = form.status.data
            with g.db as cur:
                sql = """insert into todolist(user_id, title, status,
                create_time) values ('{0}', '{1}', {2}, {3})""".format(session["id"], title, status, int(time.time()))
                cur.execute(sql)
            flash('You have add a new todo list')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/addclass', methods=['GET', 'POST'])
def add_class():
    form = NewClassForm()
    if request.method == 'GET':
        return render_template('modify.html', form=form)
    else:
        if form.validate_on_submit():
            with g.db as cur:
                sql = """insert into class_table(class_order,class_weekday,class_name,class_teacher,class_place,
                class_weekbeg,class_weekend,class_weekparity,user_id) values({0},{1},'{2}','{3}','{4}',{5},{6},{7},"{8}")
            """.format(form.class_order.data, form.class_weekday.data, form.class_name.data, form.class_teacher.data,
                       form.class_place.data, form.class_weekbeg.data, form.class_weekend.data,
                       int(form.class_weekparity.data), session["id"])
                cur.execute(sql)
            flash('You have add a class')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    form = AdminForm()
    if request.method == 'GET':
        with g.db as cur:
            sql = """select user_id,user_name,user_type,id from usertable
        """
            cur.execute(sql)
            user_list = [dict(user_id=row[0], user_name=row[1], user_type=row[2], id=row[3]) for row in
                         cur.fetchall()]

        return render_template('modify.html', form=form, user_list=user_list)
    else:

        if form.validate_on_submit():
            with g.db as cur:
                sql = """insert into usertable(user_id,user_name,user_type) values('{0}','{1}','{2}')
            """.format(form.user_id.data, form.user_name.data, form.user_type.data)
                cur.execute(sql)
            flash('You have add a user!')

        else:
            flash(form.errors)
        return redirect(url_for('admin_page'))


@app.route('/delete_user/<int:id>')
def delete_user(id):
    # id = request.args.get('id', None)
    if id is None:
        abort(404)
    else:
        sql = "delete from usertable where id = {0}".format(id)
        with g.db as cur:
            cur.execute(sql)
        flash('You have delete a user')
        return redirect(url_for('admin_page'))


@app.route('/resetpassword', methods=['GET', 'POST'])
def resetpassword():
    form = ResetPasswordForm()
    if request.method == 'GET':
        return render_template('modify.html', form=form)
    else:

        if form.validate_on_submit():

            with g.db as cur:
                sql2 = 'select * from usertable where user_id="{0}" and user_password="{1}"'.format(
                    form.user_id.data, form.user_password.data)
                cur.execute(sql2)
                infos = [dict(id=row[0]) for row in
                         cur.fetchall()]
            if infos == []:
                flash('Invalid!')
            else:
                with g.db as cur:
                    sql = """update usertable set user_password= '{0}' where user_id='{1}'
                """.format(form.user_newpassword.data, form.user_id.data)
                    cur.execute(sql)

            flash('You have resetpassword!')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/publish', methods=['GET', 'POST'])
def publish_things():
    form = PublishForm()
    if request.method == 'GET':
        with g.db as cur:
            sql = """select title,class_name,id from publishes
        """
            cur.execute(sql)
            publish_list = [dict(title=row[0], class_name=row[1], id=row[2]) for row in
                            cur.fetchall()]

        return render_template('modify.html', form=form, publish_list=publish_list)
    else:
        if form.validate_on_submit():
            with g.db as cur:
                sql = """insert into publishes(title,class_name) values('{0}','{1}')
            """.format(form.title.data, form.class_name.data)
                cur.execute(sql)
            flash('You have modify a publish')
        else:
            flash(form.errors)
        return redirect(url_for('publish_things'))


@app.route('/delete_publish/<int:id>')
def delete_publish(id):
    # id = request.args.get('id', None)
    if id is None:
        abort(404)
    else:
        sql = "delete from publishes where id = {0}".format(id)
        with g.db as cur:
            cur.execute(sql)
        flash('You have delete a publish')
        return redirect(url_for('publish_things'))


@app.route('/change/<id>', methods=['GET', 'POST'])
def change_todo_list(id):
    form = TodoListForm()
    if request.method == 'GET':
        sql = 'select id, user_id, title, status, create_time from todolist where id={0}'.format(id)
        with g.db as cur:
            cur.execute(sql)
            for row in cur.fetchall():
                todo_list = dict(id=row[0], user_id=row[1], title=row[2], status=bool(row[3]), create_time=row[4])
        form = TodoListForm()
        form.title.data = todo_list['title']
        if todo_list['status']:
            form.status.data = '1'
        else:
            form.status.data = '0'
        # print(form.status.data)
        return render_template('modify.html', form=form)
    else:
        form = TodoListForm()
        if form.validate_on_submit():
            with g.db as cur:
                sql = """update todolist set title='{0}', status='{1}'
                where id='{2}'
            """.format(form.title.data, form.status.data, id)
                # print(sql)
                cur.execute(sql)
            flash('You have modify a todolist')
        else:
            flash(form.errors)
        return redirect(url_for('show_todo_list'))


@app.route('/delete/<int:id>')
def delete_todo_list(id):
    # id = request.args.get('id', None)
    if id is None:
        abort(404)
    else:
        sql = "delete from todolist where id = {0}".format(id)
        with g.db as cur:
            cur.execute(sql)
        flash('You have delete a todo list')
        return redirect(url_for('show_todo_list'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        session['id'] = request.form['username']
        if session['id'] == app.config['USERNAME'] and request.form['password'] == app.config['PASSWORD']:
            session['logged_in'] = True
            session['type'] = "admin"
            session['name'] = "管理员A"
            return redirect(url_for('admin_page'))
        sql = 'select user_id,user_name,user_type,user_password from usertable where user_id="{0}"'.format(
            session['id'])
        with g.db as cur:
            cur.execute(sql)
            infos = [dict(user_id=row[0], user_name=row[1], user_type=row[2], user_password=row[3]) for row in
                     cur.fetchall()]
        if infos == []:
            flash('Invalid username')
        elif request.form['password'] != infos[0]["user_password"]:
            flash('Invalid password')
        else:
            session['logged_in'] = True
            session['type'] = infos[0]["user_type"]
            session['name'] = infos[0]["user_name"]
            flash('you have logged in!')
            return redirect(url_for('show_todo_list'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('id', None)
    session.pop('type', None)
    session.pop('name', None)
    flash('you have logout!')
    return redirect(url_for('login'))


if __name__ == '__main__':
    manager.run()
