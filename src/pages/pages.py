from flask import abort, Blueprint, render_template

bp = Blueprint('pages', __name__, template_folder='templates') 

@bp.route('/', defaults={'page': 'index'})
@bp.route('/<page>')
def get_page(page):
    try:
        return render_template('%s.html' % page)
    except:
        abort(404)