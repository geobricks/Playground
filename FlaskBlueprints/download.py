from flask import Blueprint

download = Blueprint('download', __name__)

@download.route('/download')
def index():
    return 'Welcome to the Download module!'