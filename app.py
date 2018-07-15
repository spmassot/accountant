from flask import Flask
from flask import render_template, url_for
from views import index, load, generate


app = Flask(__name__)

app.register_blueprint(index.routes)
app.register_blueprint(load.routes)
app.register_blueprint(generate.routes)
