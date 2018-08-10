from dotenv import load_dotenv
from datetime import timedelta
from flask import (
    Flask, session, render_template, request, flash, redirect, url_for
)
from os import getenv
import logging
import logging.handlers

from views import index, load, generate
import src.user
from src.interfaces import s3
from src.db import Database


load_dotenv()
application = Flask(__name__)
application.secret_key = getenv('AUTH_KEY')
session_timeout = int(getenv('SESSION_TIMEOUT_IN_MINUTES'))
application.permanent_session_lifetime = timedelta(minutes=session_timeout)
s3.initialize_bucket(getenv('FILE_BUCKET'))
user.initialize_users()

# Database.initialize()

modules = [index, load, generate]
for module in modules:
    application.register_blueprint(module.routes)


def log(msg):
    logging.basicConfig(
        format='%(asctime)s --- %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )
    logging.info('%s', msg)


def authorize(username, password):
    if not user.is_valid_login(username, password):
        return False
    session.permanent = True
    session['username'] = username
    return True


def is_logged_in():
    if session.get('username'):
        return True
    return False


@application.before_request
def before_request():
    if not is_logged_in():
        if not authorize(
            request.form.get('username'),
            request.form.get('password')
        ):
            flash('Invalid login information', 'error')
            return render_template('login.html')


@application.route('/login', methods=['POST'])
def login():
    if authorize(
        request.form.get('username'),
        request.form.get('password')
    ):
        return redirect(url_for('index.index'))
    else:
        flash('Invalid login information', 'error')
        return render_template('login.html')


@application.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return render_template('login.html')


if __name__ == '__main__':
    application.run()
