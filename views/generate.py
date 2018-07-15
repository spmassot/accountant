from flask import Blueprint, render_template

routes = Blueprint('generate', __name__)

@routes.route('/generate')
def index():
    return render_template('generate.html')

