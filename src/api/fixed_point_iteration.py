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
        import logging
        logging.critical(f + "|" + str(a) + "-" + str(b) )
        if a >= b:
            return False
        try:
            FixedPointIteration.get_val(f, a)
        except (NameError, SyntaxError):
            return False

        return True

    @staticmethod
    def get_n0(f, lamb, x, a, b, eps):
        if not FixedPointIteration.check_f_a_b(f, a, b):
            return 0
        if x < a or b < x:
            return 0
        try:
            val = abs(FixedPointIteration.get_val(f, x) * FixedPointIteration.get_val(lamb, x))
            delta = max(x - a, b - x)
            q = 1 - val / delta
            n0 = int(
                np.abs(
                    np.log(
                        val / ((1 - q) * eps)
                    ) /
                    np.log(1 / q)
                )
            ) + 2
            return n0
        except (NameError, SyntaxError, ValueError):
            return 0


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

        return res

    @staticmethod
    def get_answer(f, lamb, a, b, x0, iter_count):
        if a >= b:
            return 'Error. A must be less than B', 0
        if x0 < a or b < x0:
            return 'Error. x0 must lie inside of [A; B]', 0

        iter_passed_count = 0
        try:
            x = x0
            for i in range(iter_count):
                iter_passed_count += 1
                x = x - FixedPointIteration.get_val(lamb, x) * FixedPointIteration.get_val(f, x)
                if x < a or b < x:
                    return 'Error. Convergence of function is bad.', iter_passed_count

        except (NameError, SyntaxError):
            return 'Error in your function. Maybe you did something wrong...?', iter_passed_count

        return float(x), iter_passed_count

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

        sol = FixedPointIteration.get_answer(f, lamb, a, b, x0, iter_count)[0]

        if type(sol) is not str:
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
    n0 = FixedPointIteration.get_n0(
        form.f.data,
        form.lamb.data,
        form.x0.data,
        form.left_bound.data,
        form.right_bound.data,
        form.eps.data
    )
    return FixedPointIteration.get_img(
        form.f.data,
        form.lamb.data,
        form.left_bound.data,
        form.right_bound.data,
        form.x0.data,
        n0,
        form.tracing.data,
        form.w.data,
        form.h.data
    )


def get_answer(form):
    n0 = FixedPointIteration.get_n0(
        form.f.data,
        form.lamb.data,
        form.x0.data,
        form.left_bound.data,
        form.right_bound.data,
        form.eps.data
    )
    ans = FixedPointIteration.get_answer(
        form.f.data,
        form.lamb.data,
        form.left_bound.data,
        form.right_bound.data,
        form.x0.data,
        n0
    )

    if type(ans[0]) is not float:
        return '%s \n' \
               ' Passed iterations: %d' % ans
    return 'Solution: %.9f \n' \
           'Count of iterations: %d' % ans


methods = {
    'img': get_img,
    'ans': get_answer
}