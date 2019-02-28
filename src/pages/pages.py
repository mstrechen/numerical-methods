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
