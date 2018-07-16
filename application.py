from dotenv import load_dotenv
from flask import Flask
from os import getenv
import logging
import logging.handlers

from flask import render_template, url_for
from views import index, load, generate
from interfaces import s3


application = Flask(__name__)
load_dotenv()

application.register_blueprint(index.routes)
application.register_blueprint(load.routes)
application.register_blueprint(generate.routes)

s3.initialize_bucket(getenv('FILE_BUCKET'))

def log(msg):
    logging.basicConfig(
        format='%(asctime)s --- %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=logging.INFO
    )
    logging.info('%s', msg)

if __name__ == '__main__':
    application.run()
