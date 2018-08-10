from flask import Blueprint, redirect, request
from src.file_prep import prep_files
from src.interfaces import s3

routes = Blueprint('load', __name__, url_prefix='/load')


@routes.route('/new', methods=['POST'])
def file_upload_handler():

    file_type = request.form.get('file_type')
    input_files = request.files.to_dict(flat=False).get('input_files')

    for input_file in input_files:
        prepped_file = prep_file(input_file, file_type)
        load_file(prepped_file, file_type)

    return redirect('/')
