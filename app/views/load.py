from flask import Blueprint, redirect, request, flash
from src.file_prep import prep_file
from src.file_load import load_file
from src.interfaces import s3
import src.logger as log

routes = Blueprint('load', __name__, url_prefix='/load')


@routes.route('/new', methods=['POST'])
def file_upload_handler():

    file_type = request.form.get('file_type')
    input_files = request.files.to_dict(flat=False).get('input_files')

    for input_file in input_files:
        #try:
           prepped_file = prep_file(input_file, file_type)
           load_file(input_file.filename, prepped_file, file_type)
        #except Exception as err:
        #   log.error(err)
        #   flash(str(err))

    return redirect('/')
