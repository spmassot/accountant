from flask import Flask
from flask import render_template, url_for
from views import index


app = Flask(__name__)

app.register_blueprint(index.routes)
