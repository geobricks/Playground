__package__ = 'FlaskBlueprints'
__author__ = 'Guido Barbaglia'
__email__ = 'guido.barbaglia@gmail.com'
__license__ = 'GPL2'

from flask import Flask
from browse import browse
from download import download
import config

app = Flask(__name__)
app.register_blueprint(browse)
app.register_blueprint(download)

config = config