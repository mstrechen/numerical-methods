from werkzeug.datastructures import CombinedMultiDict

from flask import abort, Blueprint, request
import logging

import dichotomy_method

import forms

bp = Blueprint('api', __name__, url_prefix='/api') 


@bp.route('/dichotomy-method/<method>')
def dichotomy_solve(method):
    form = forms.DichotomyForm(request.args)
    try:
        return dichotomy_method.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.log(logging.CRITICAL, str(ex))
        abort(400)
