from flask import Flask

from api import api
from pages import pages

def configure_app():
    app = Flask(__name__, static_url_path='/static', static_folder='static')
    app.register_blueprint(api.bp)
    app.register_blueprint(pages.bp)

    return app