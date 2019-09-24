from flask import abort, Blueprint, render_template
from jinja2.exceptions import TemplateNotFound

bp = Blueprint('pages', __name__, template_folder='templates')

pages_list = [
    {
        "page": "dichotomy-method",
        "headline": "Dichotomy (Bisection method)",
        "text": "Dichotomy (or Bisection) method is a root-finding "
                "method that applies to any continuous functions for "
                "which one knows two values with opposite signs.",
    },
    {
        "page": "fixed-point-iteration",
        "headline": "Fixed-point iteration",
        "text": "Fixed-point iteration is a method of computing fixed points "
                "of iterated functions. It can be also applied for finding the "
                "root of continuous function"
    },

    {
        "page": "linear-system",
        "headline": "System of linear equations",
        "text": "System of linear equations is a collection "
                "of two or more linear equations involving the same set of variables." 
                "We will take a look at 2 methods of solving linear systems: Gaussian" 
                "elimination and Jacobi method"
    },
    {
        "page": "unnamed-matrix",
        "headline": "Unnamed matrix",
        "text": "This is not a general method or something. It is required just to get the matrix based on some characteristics."
    },
    {
        "page": "intersection-of-surfaces",
        "headline": "Intersection of surfaces",
        "text": "Intersection of surfaces... Ellipsoid and the plane."
    },
    {
        "page": "cubic-splines",
        "headline": "Cubic splines",
        "text": "Cubic splines method is one of dozens methods of function interpolating."
    },
    {
        "page" : "chebyshev-aproximation",
        "headline": "Chebyshev polynoms & approximation",
        "Text": "Approximation of function using chebyshev polynoms",
    }

]


@bp.route('/', defaults={'page': 'index'})
@bp.route('/<page>')
def get_page(page):
    try:
        if page == 'index':
            return render_template('index.html', pages=pages_list)
        else:
            return render_template('%s.html' % page)
    except TemplateNotFound:
        abort(400)
