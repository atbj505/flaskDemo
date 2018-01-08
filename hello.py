#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, request, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess'
app.config[
    'SQLALCHEMY_DATABASE_URI'] = 'mysql://root:robert080904@localhost:3306/hello?charset=utf8'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    user = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role {}> '.format(self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/hello')
def hello_world():
    return 'Hello World!'


@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)


@app.route('/user/<user_name>')
def show_user_profile(user_name):
    return 'User %s' % user_name


@app.route('/post/<int:post_id>')
def show_post(post_id):
    return 'Post %d' % post_id


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return url_for('login', method='POST')
    else:
        return url_for('login', method='GET')


if __name__ == "__main__":
    app.debug = True
    app.run()
