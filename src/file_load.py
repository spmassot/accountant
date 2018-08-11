from src.interfaces import s3
from datetime import datetime as dt


def load_file(file_name, file_data, file_type):
    object_name = ''.join(file_name.split('.')[:-1])
    {
        'ups': load_ups_file,
        'givens': load_givens_file,
        'freight': load_freight_report_file
    }.get(file_type)(object_name, file_data)


def load_ups_file(file_name, ups_file):
    if f'ups/{file_name}' not in s3.list_objects():
        s3.put_file_in_folder(file_name, ups_file, 'ups')


def load_givens_file(file_name, givens_file):
    if f'givens/{file_name}' not in s3.list_objects():
        s3.put_file_in_folder(file_name, givens_file[0], 'givens')
    if f'givens_adjustments/{file_name}' not in s3.list_objects():
        s3.put_file_in_folder(file_name, givens_file[1], 'givens_adjustments')


def load_freight_report_file(file_name, freight_report_file):
    if f'freight_report/{file_name}' not in s3.list_objects():
        s3.put_file_in_folder(file_name, freight_report_file, 'freight_report')
