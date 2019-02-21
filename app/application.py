from dotenv import load_dotenv
from datetime import timedelta
from flask import (
    Flask, session, render_template, request, flash, redirect, url_for
)
from os import getenv
import logging

from views import index, load, generate
import src.user as user
from src.interfaces import s3


load_dotenv()
application = Flask(__name__)

application.logger.handlers = []
application.logger.addHandler(logging.StreamHandler())

application.secret_key = getenv('AUTH_KEY')
session_timeout = int(getenv('SESSION_TIMEOUT_IN_MINUTES'))
application.permanent_session_lifetime = timedelta(minutes=session_timeout)
s3.initialize_bucket(getenv('FILE_BUCKET'))
user.initialize_users()


modules = [index, load, generate]
for module in modules:
    application.register_blueprint(module.routes)


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
    application.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
