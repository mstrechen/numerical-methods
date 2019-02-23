from flask import Flask

from api import api
from pages import pages

from werkzeug.contrib.fixers import ProxyFix

def configure_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.register_blueprint(api.bp)
    app.register_blueprint(pages.bp)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    return app