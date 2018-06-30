#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import (Flask, abort, current_app, redirect, render_template,
                   request, url_for, session, flash)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager, Shell
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField
from wtforms.validators import Required
from flask_migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:robert080904@localhost:3306/flaskr_web?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, User=User, Role=Role)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command("db", MigrateCommand)


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %s>' % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %s>' % self.username


class NameForm(FlaskForm):
    name = StringField("What 's your name?", validators=[Required()])
    submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '<h1>Hello %s %s %s!</h1>' % (user_agent, current_app.name,
    # app.url_map)
    # return '<h1>Bad Request</h1>', 400
    # return redirect('http://github.com')
    # return render_template('index.html', current_time=datetime.utcnow())
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if not user:
            user = User(username=form.name.data, role_id=1)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template(
        'index.html',
        form=form,
        name=session.get('name'),
        known=session.get('known'))


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
    # return url_for('user', name='robert', page=2, _external=True)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    manager.run()
