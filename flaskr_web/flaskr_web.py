#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_script import Manager
from flask.ext.moment import Moment
from flask.ext.bootstrap import Bootstrap
from flask import request, current_app
from flask import redirect, abort
from flask import render_template, url_for
app = Flask(__name__)
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route('/')
def index():
    # user_agent = request.headers.get('User-Agent')
    # return '<h1>Hello %s %s %s!</h1>' % (user_agent, current_app.name,
    # app.url_map)
    # return '<h1>Bad Request</h1>', 400
    # return redirect('http://github.com')
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    # return render_template('user.html', name=name)
    return url_for('user', name='robert', page=2, _external=True)


if __name__ == "__main__":
    manager.run()
