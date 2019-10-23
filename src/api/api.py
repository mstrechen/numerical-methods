from flask import abort, Blueprint, request, jsonify
import logging

from . import dichotomy_method
from . import fixed_point_iteration
from . import linear_systems
from . import unnamed_matrix
from . import intersection_of_surfaces
from . import cubic_splines
from . import chebyshev_aprox
from . import pelengate_problem
from . import runge_kutta
from . import runge_kutta_pendulum


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
    
@bp.route('/linear-systems/<method>')
def linear_systems_solve(method):
    form = forms.LinearSystems (request.args)
    try:
        return linear_systems.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/unnamed-matrix/<method>')
def unnamed_matrix_solve(method):
    form = forms.UnnamedMatrixForm(request.args, csrf_enabled=False)
    if not form.validate():
        logging.critical("FORM FAILED", str(form.errors))
        abort(400, form.errors) 
    try:
        return unnamed_matrix.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/intersection_of_surfaces/<method>')
def intersection_of_surfaces_solve(method):
    try:
        return jsonify(intersection_of_surfaces.methods[method]())
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)

@bp.route('/cubic-splines/<method>')
def cubic_splines_solve(method):
    form = forms.CubicSplinesForm(request.args)
    logging.critical(form)
    try:
        return cubic_splines.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/chebyshev-aprox/<method>')
def chebyshev_aprox_solve(method):
    form = forms.ChebyshevApproxForm(request.args)
    try:
        return chebyshev_aprox.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/pelengate-problem/<method>')
def pelengate_problem_solve(method):
    form = forms.PelengateProblem(request.args)
    print(form.validate(), flush=True)
    try:
        return pelengate_problem.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/runge-kutta/<method>')
def runge_kutta_method(method):
    form = forms.RungeKuttaForm(request.args)
    try:
        return runge_kutta.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)


@bp.route('/runge-kutta-pendulum/<method>')
def runge_kutta_pendulum_endpoint(method):
    form = forms.RungeKuttaPendulumForm(request.args)
    print(form, flush=True)
    try:
        return runge_kutta_pendulum.methods[method](form)
    except KeyError:
        abort(404)
    except Exception as ex:
        logging.critical(str(type(ex)) + str(ex))
        abort(400)