from flask import Blueprint, redirect, request
from filer import prep_files
from interfaces import s3

routes = Blueprint('load', __name__, url_prefix='/load')


@routes.route('/new', methods=['POST'])
def file_upload_handler():
    # s3.load(
    #     prep_files(request.files, request.file_type),
    # )
    print(s3.all_buckets())
    return redirect('/')
