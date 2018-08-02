from flask import Blueprint, render_template
from interfaces import s3

routes = Blueprint('generate', __name__)

@routes.route('/generate')
def index():
    return render_template('generate.html')


@routes.route('/generate/new', methods=['POST'])
def handle_new():
    s3.create_folder('farts')
    s3.put_file_in_folder('farts.txt', 'pfvfvfvfvft', 'farts')
    return render_template('index.html')
