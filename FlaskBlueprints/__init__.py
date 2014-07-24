from flask import Flask
from browse import browse
from download import download
import config

app = Flask(__name__)
app.register_blueprint(browse)
app.register_blueprint(download)

config = config