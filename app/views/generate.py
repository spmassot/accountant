from flask import Blueprint, render_template


routes = Blueprint('generate', __name__, url_prefix='/generate')


@routes.route('/')
def index():
    return render_template('generate.html')


@routes.route('/new', methods=['POST'])
def handle_new():
    return render_template('index.html')
