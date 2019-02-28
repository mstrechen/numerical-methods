from flask import abort, Blueprint, request
import logging

from . import dichotomy_method
from . import fixed_point_iteration


from . import forms

bp = Blueprint('api', __name__, url_prefix='/api') 


@bp.route('/dichotomy-method/<method>')
def dichotomy_solve(method):
    form = forms.DichotomyForm(request.args)
    try:
        return dichotomy_method.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/fixed-point-iteration/<method>')
def fixed_point_iter_solve(method):
    form = forms.FixedPointIterationForm(request.args)
    try:
        return fixed_point_iteration.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)
