from flask import Blueprint, render_template

routes = Blueprint('index', __name__)

@routes.route('/')
def about():
    return render_template('index.html')
