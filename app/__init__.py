import os

from flask import Flask

UPLOAD_FOLDER = 'files'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(os.getcwd(), UPLOAD_FOLDER)

if app:
    import routs

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
