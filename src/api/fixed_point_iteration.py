from flask import make_response, send_from_directory

import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from io import StringIO, BytesIO

import numpy as np


class FixedPointIteration:
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
        names = FixedPointIteration.ALLOWED_FUNCTIONS.copy()
        names['x'] = x
        return eval(f, {'__builtins__': None}, names)

    @staticmethod
    def check_f_a_b(f, a, b):
        if a >= b:
            return False
        try:
            FixedPointIteration.get_val(f, a)
        except (NameError, SyntaxError):
            return False

        return True

    @staticmethod
    def get_answer_seq(f, lamb, a, b, x0, iter_count):
        res = [x0]
        if a >= b:
            return res
        if x0 < a or b < x0:
            return res
        try:
            x = x0
            for i in range(iter_count):
                x = x - FixedPointIteration.get_val(lamb, x) * FixedPointIteration.get_val(f, x)
                if x < a or b < x:
                    return res
                res.append(x)

        except (NameError, SyntaxError):
            return res
        import logging

        return res

    @staticmethod
    def get_answer(f, lamb, a, b, x0, iter_count):
        if a >= b:
            return 'Error. A must be less than B'
        if x0 < a or b < x0:
            return 'Error. x0 must lie inside of [A; B]'
        try:
            x = x0
            for i in range(iter_count):
                x = x - FixedPointIteration.get_val(lamb, x) * FixedPointIteration.get_val(f, x)
                if x < a or b < x:
                    return 'Error. Convergence of function is bad.'

        except (NameError, SyntaxError):
            return 'Error in your function. Maybe you did something wrong...?   '

        return float(x)

    @staticmethod
    def error_img():
        return send_from_directory('static/img', 'math-error.jpg')

    @staticmethod
    def draw_default_fig(w, h, a, b):
        fig = plt.figure(
            figsize=(w / FixedPointIteration.DPI,
                     h / FixedPointIteration.DPI), dpi=FixedPointIteration.DPI * 4)

        graphic = fig.add_subplot(1, 1, 1)
        graphic.grid()
        graphic.hlines(0, a, b)

        return fig, graphic

    @staticmethod
    def draw_graphic(f, lamb, a, b, x0, iter_count, tracing, w, h):
        fig, graphic = FixedPointIteration.draw_default_fig(w, h, a, b)

        X = np.linspace(a, b, w)
        Y = FixedPointIteration.get_val(f, X)

        graphic.plot(X, Y, 'b-', zorder=1)

        if tracing:
            res = FixedPointIteration.get_answer_seq(f, lamb, a, b, x0, iter_count)
            res = np.array(res)
            resy = FixedPointIteration.get_val(f, res)
            graphic.scatter(res, resy, color='g', zorder=4, alpha=0.3)

        sol = FixedPointIteration.get_answer(f, lamb, a, b, x0, iter_count)
        graphic.scatter([sol], [0], color='y', zorder=5)

        return fig

    @staticmethod
    def get_img(f, lamb, a, b, x0, iter_count, tracing, w, h):
        if not FixedPointIteration.check_f_a_b(f, a, b):
            return FixedPointIteration.error_img()

        fig = FixedPointIteration.draw_graphic(f, lamb, a, b, x0, iter_count, tracing, w, h)

        output = BytesIO()
        fig.savefig(output, format='png')

        response = make_response(output.getvalue())
        response.mimetype = 'image/png'

        return response


def get_img(form):
    return FixedPointIteration.get_img(
        form.f.data,
        form.lamb.data,
        form.left_bound.data,
        form.right_bound.data,
        form.x0.data,
        form.iter_count.data,
        form.tracing.data,
        form.w.data,
        form.h.data
    )


def get_answer(form):
    ans = FixedPointIteration.get_answer(
        form.f.data,
        form.lamb.data,
        form.left_bound.data,
        form.right_bound.data,
        form.x0.data,
        form.iter_count.data,
    )

    if type(ans) is not float:
        return ans
    return '%.9f' % ans


methods = {
    'img': get_img,
    'ans': get_answer
}