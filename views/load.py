from flask import Blueprint, render_template

routes = Blueprint('load', __name__)

@routes.route('/load')
def index():
    return render_template('load.html')
