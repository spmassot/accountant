from src.interfaces import s3
from src.db import Database as db
from datetime import datetime as dt


def load_file(file_name, file_data, file_type):
    object_name = ''.join(file_name.split('.')[:-1])
    {
        'ups': load_ups_file,
        'givens': load_givens_file,
        'freight': load_freight_report_file
    }.get(file_type)(object_name, file_data)


def load_ups_file(file_name, ups_file):
    if not db.check_history('ups_invoice', file_name):
        db.execute_query(db.qb.bulk_insert('ups_invoice_row', ups_file))
        db.update_history('ups_invoice', file_name)


def load_givens_file(file_name, givens_file):
    if not db.check_history('givens_invoice', file_name):
        db.execute_query(db.qb.bulk_insert('givens', givens_file[0]))
        db.execute_query(db.qb.bulk_insert('givens_adjustments', givens_file[1]))
        db.update_history('givens_invoice', file_name)


def load_freight_report_file(file_name, freight_report_file):
    if not db.check_history('frieght_report', file_name):
        db.execute_query(db.qb.bulk_insert('frieght_report_row', freight_report_file))
        db.update_history('frieght_report', file_name)
