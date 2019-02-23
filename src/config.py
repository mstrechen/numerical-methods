import os

from flask import Flask

from api import api
from pages import pages

from werkzeug.contrib.fixers import ProxyFix

def get_bool_flag(key):
    val = os.environ.get(key, False)
    return val in ['1', 'true', 'True', 'TRUE']

def configure_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.register_blueprint(api.bp)
    app.register_blueprint(pages.bp)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    app.config['DEBUG'] = get_bool_flag('DEBUG')

    return app