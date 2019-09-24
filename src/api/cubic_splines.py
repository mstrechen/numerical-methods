from flask import make_response, send_from_directory
import logging
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from io import StringIO, BytesIO

import numpy as np


class CubicSplines:
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
        names = CubicSplines.ALLOWED_FUNCTIONS.copy()
        names['x'] = x
        return eval(f, {'__builtins__': None}, names)


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
                x = x - CubicSplines.get_val(lamb, x) * CubicSplines.get_val(f, x)
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
                x = x - CubicSplines.get_val(lamb, x) * CubicSplines.get_val(f, x)
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
            figsize=(w / CubicSplines.DPI,
                     h / CubicSplines.DPI), dpi=CubicSplines.DPI * 4)

        graphic = fig.add_subplot(1, 1, 1)
        graphic.grid()
        graphic.hlines(0, a, b)

        return fig, graphic

    @staticmethod
    def get_cubic_value(x, a, b, c, d):
        return a + b*x + c*x*x + d*x*x*x

    @staticmethod
    def get_cubic_spline(x, y):
        n = len(x) - 1
        h = [x[i + 1] - x[i] for i in range(n)]
        al = [3 * ((y[i + 1] - y[i]) / h[i] - (y[i] - y[i - 1]) / h[i - 1]) for i in range(1, n)]
        al.insert(0, 0)

        l = [1] * (n + 1)
        u = [0] * (n + 1)
        z = [0] * (n + 1)
        for i in range(1, n):
            l[i] = 2 * (x[i + 1] - x[i - 1]) - h[i - 1] * u[i - 1]
            u[i] = h[i] / l[i]
            z[i] = (al[i] - h[i - 1] * z[i - 1]) / l[i]

        b = [0] * (n + 1)
        c = [0] * (n + 1)
        d = [0] * (n + 1)
        for i in range(n - 1, -1, -1):  # for i in reversed(range(n)):
            c[i] = z[i] - u[i] * c[i + 1]
            b[i] = (y[i + 1] - y[i]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
            d[i] = (c[i + 1] - c[i]) / (3 * h[i])
        return np.array([y, b, c, d], dtype='float64')

    @staticmethod
    def draw_graphic(f, a, b, N, w, h):
        fig, graphic = CubicSplines.draw_default_fig(w, h, a, b)

        X = np.linspace(a, b, w)
        Y = CubicSplines.get_val(f, X)

        graphic.plot(X, Y, 'b-', zorder=1)

        x_basic = np.linspace(a, b, N + 1)            
        y_basic = CubicSplines.get_val(f, x_basic)
        graphic.scatter(x_basic, y_basic, color='g', zorder=4, alpha=0.3)

        spline = CubicSplines.get_cubic_spline(x_basic, y_basic)
        
        x_res = np.array([])
        y_res = np.array([])
        for i in range(int(N)):
            xx = np.linspace(x_basic[i], x_basic[i+1], 100)
            yy = CubicSplines.get_cubic_value(xx - x_basic[i], spline[0][i], spline[1][i], spline[2][i], spline[3][i])
            x_res = np.append(x_res, xx)
            y_res = np.append(y_res, yy)

        graphic.plot(x_res, y_res, 'r--', zorder=6)


        return fig

    @staticmethod
    def get_img(f, a, b, N, w, h):
        fig = CubicSplines.draw_graphic(f, a, b, N, w, h)

        output = BytesIO()
        fig.savefig(output, format='png')

        response = make_response(output.getvalue())
        response.mimetype = 'image/png'

        return response


def get_img(form):
    return CubicSplines.get_img(
        form.f.data,
        form.left_bound.data,
        form.right_bound.data,
        form.N.data,
        form.w.data,
        form.h.data
    )

methods = {
    'img': get_img
}