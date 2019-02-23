#!/bin/python3

import os

from config import configure_app

app = configure_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)