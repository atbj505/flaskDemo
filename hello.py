#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, url_for, request, render_template
app = Flask(__name__)


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
