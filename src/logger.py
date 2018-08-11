from flask import current_app as app
from io import StringIO
import traceback


def error(msg):
    error_buffer = StringIO()
    traceback.print_exc(file=error_buffer)
    error_message = error_buffer.getvalue()
    app.logger.error(msg)


def info(msg):
    app.logger.info(msg)
