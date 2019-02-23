#!/bin/python3

import os

from config import configure_app

app = configure_app()

def get_bool_flag(key):
    val = os.environ.get(key, False)
    return val in ['1', 'true', 'True', 'TRUE']

if __name__ == '__main__':
    debug = get_bool_flag('DEBUG')
    app.run(debug=debug, host='0.0.0.0', port=8080)