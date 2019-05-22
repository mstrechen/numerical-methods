from flask import make_response, send_from_directory

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt


from io import StringIO, BytesIO

import numpy as np


class DichotomyMethod:
    ALLOWED_FUNCTIONS = {
        'max': np.fmax,
        'min': np.fmin,
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'arcsin': np.arcsin,
        'arccos': np.arccos,
        'hypot': np.hypot,
        'arctan2': np.arctan2,
        'exp': np.exp,
        'log': np.log,
        'log10': np.log10,
        'log1p': np.log1p,
        'pow': np.power,
        'sqrt': np.sqrt,
        'cbrt': np.cbrt,
        'abs': np.fabs,
        'sgn': np.sign
    }
    DPI = 96

    @staticmethod
    def get_val(f, x):
        names = DichotomyMethod.ALLOWED_FUNCTIONS.copy()
        names['x'] = x
        return eval(f, {'__builtins__': None}, names)

    @staticmethod
    def check_f_a_b(f, a, b):
        if a >= b:
            return False
        try:
            DichotomyMethod.get_val(f, a)
        except (NameError, SyntaxError):
            return False

        return True

    @staticmethod
    def get_answer(f, a, b, eps):
        if eps < 1e-9:
            return 'Error. Epsilon must be greater than 0.000\'000\'001'
        if a >= b:
            return 'Error. A must be less than B'
        try:
            if DichotomyMethod.get_val(f, a) * DichotomyMethod.get_val(f, b) > 0:
                return 'Error. f(a) * f(b) must be not greater than zero.'
        except (NameError, SyntaxError):
            return 'Error in your function. Maybe you did something wrong...?   '
            
        iter_count = 0
        while a + eps < b:
            mid = (a + b) / 2
            if DichotomyMethod.get_val(f, a) * DichotomyMethod.get_val(f, mid) <= 0:
                b = mid
            else:
                a = mid
            iter_count += 1
        return (a + b) / 2, iter_count

    @staticmethod
    def error_img():
        return send_from_directory('static/img', 'math-error.jpg')

    @staticmethod
    def draw_default_fig(w, h, a, b):
        fig = plt.figure(
            figsize=(w / DichotomyMethod.DPI,
                     h / DichotomyMethod.DPI), dpi=DichotomyMethod.DPI * 4)

        graphic = fig.add_subplot(1, 1, 1)
        graphic.grid()
        graphic.hlines(0, a, b)

        return fig, graphic

    @staticmethod
    def draw_graphic(f, a, b, w, h, res):
        fig, graphic = DichotomyMethod.draw_default_fig(w, h, a, b)

        X = np.linspace(a, b, w)
        Y = DichotomyMethod.get_val(f, X)

        graphic.plot(X, Y, 'b-', zorder=1)

        px = np.array([a, b])
        py = DichotomyMethod.get_val(f, px)
        graphic.scatter(px, py, marker='x', color='r', zorder=3)

        if type(res) is not str:
            res = res[0]
            graphic.scatter(np.array([res]), np.array([0]), color='g', zorder=4)

        return fig

    @staticmethod
    def get_img(f, a, b, eps, w, h):
        res = DichotomyMethod.get_answer(f, a, b, eps)
        if not DichotomyMethod.check_f_a_b(f, a, b):
            return DichotomyMethod.error_img()

        fig = DichotomyMethod.draw_graphic(f, a, b, w, h, res)

        output = BytesIO()
        fig.savefig(output, format='png')

        response = make_response(output.getvalue())
        response.mimetype = 'image/png'

        return response


def get_img(form):
    return DichotomyMethod.get_img(
        form.f.data,
        form.left_bound.data,
        form.right_bound.data,
        form.eps.data,
        form.w.data,
        form.h.data
        )


def get_answer(form):
    ans = DichotomyMethod.get_answer(
        form.f.data,
        form.left_bound.data,
        form.right_bound.data,
        form.eps.data
    )
    if type(ans) is str:
        return ans
    return 'Solution: %.9f \n' \
           'Count of iterations: %d' % ans


methods = {
    'img': get_img,
    'ans': get_answer
}