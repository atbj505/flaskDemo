#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime

from flask import (Flask, abort, current_app, redirect, render_template,
                   request, url_for, session, flash)
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_script import Manager
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


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
        old_name = session.get('name')
        if old_name and old_name != form.name.data:
            flash("Look like you have changed your name!")
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


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
