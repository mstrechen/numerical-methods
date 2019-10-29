from flask import make_response, send_from_directory, jsonify
import logging
import matplotlib

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from io import StringIO, BytesIO

import numpy as np

from numpy.polynomial import Polynomial

from .forms import RungeKuttaPendulumForm


class RungeKutta:
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

    SAVED_CHEBYSHEV_POLYNOMIALS = {
        0: Polynomial([1]),
        1: Polynomial([0, 1]),
    }

    @classmethod
    def get_chebyshev_polynomial(cls, i):
        if i in cls.SAVED_CHEBYSHEV_POLYNOMIALS:
            return cls.SAVED_CHEBYSHEV_POLYNOMIALS[i]
        cls.SAVED_CHEBYSHEV_POLYNOMIALS[i] = \
            - cls.get_chebyshev_polynomial(i - 2) \
            + cls.get_chebyshev_polynomial(i - 1) * Polynomial([0, 2])
        return cls.SAVED_CHEBYSHEV_POLYNOMIALS[i]

    @staticmethod
    def get_val(f, **kwargs):
        names = RungeKutta.ALLOWED_FUNCTIONS.copy()
        names.update(kwargs)
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
                x = x - RungeKutta.get_val(lamb, x=x, y=0) * RungeKutta.get_val(f, x=x, y=0)
                if x < a or b < x:
                    return res
                res.append(x)

        except (NameError, SyntaxError):
            return res

        return res


    @staticmethod
    def error_img():
        return send_from_directory('static/img', 'math-error.jpg')

    @staticmethod
    def draw_default_fig(w, h, a, b):
        fig = plt.figure(
            figsize=(w / RungeKutta.DPI,
                     h / RungeKutta.DPI), dpi=RungeKutta.DPI * 4)

        graphic = fig.add_subplot(1, 1, 1)
        graphic.grid()
        graphic.hlines(0, a, b)

        return fig, graphic

    @classmethod
    def get_approach(cls, h, xprev, yprev, f, g_const, l_const):
        k1 = cls.get_val(f, x=xprev, y=yprev, g=g_const, l=l_const)
        k2 = cls.get_val(f, x=xprev + h / 2, y=yprev + h * k1 / 2, g=g_const, l=l_const)
        k3 = cls.get_val(f, x=xprev + h / 2, y=yprev + h * k2 / 2, g=g_const, l=l_const)
        k4 = cls.get_val(f, x=xprev + h, y=yprev + h * k3, g=g_const, l=l_const)
        return h * (k1 + 2*k2 + 2*k3 + k4) / 6


    @classmethod
    def get_runge_kutta(cls, tfin, x0, y0, N, f, g, g_const, l_const):
        h = (tfin - x0) / N
        t = [0]
        x = [x0]
        y = [y0]
        for i in range(N):
            tprev = t[-1]
            xprev, yprev = x[-1], y[-1]
            xnew = xprev + cls.get_approach(h, xprev, yprev, f, g_const, l_const)
            ynew = yprev + cls.get_approach(h, xprev, yprev, g, g_const, l_const)
            t.append(tprev + h)
            x.append(xnew)
            y.append(ynew)

        return np.array(t), np.array(x), np.array(y)

    @classmethod
    def draw_graphic(cls, f_func, a, b, N, w, h, g_func, x0, y0, g_const, l_const):
        a = 0
        b = abs(b)

        fig, graphic = RungeKutta.draw_default_fig(w, h, a, b)

        # X = np.linspace(a, b, w)
        # Y = RungeKutta.get_val(func_exp, x=X)

        #graphic.plot(X, Y, 'b-', zorder=1)

        t, x, y = cls.get_runge_kutta(b, x0, y0, N, f_func, g_func, g_const, l_const)
        graphic.plot(t, x, 'r--', zorder=6)
        graphic.plot(t, y, 'b--', zorder=6)

        graphic.scatter([x0], [y0], color='g')

        return fig
        
    @classmethod
    def get_coords(cls, f_func, a, b, N, w, h, g_func, x0, y0, g_const, l_const):
        a = 0
        b = abs(b)

        t, x, y = cls.get_runge_kutta(b, x0, y0, N, f_func, g_func, g_const, l_const)

        return jsonify({'t': t.tolist(), 'x': x.tolist(), 'y': y.tolist()})

    @classmethod
    def get_img(cls,f, a, b, N, w, h, g_func, x0, y0, g_const, l_const):
        fig = cls.draw_graphic(f, a, b, N, w, h, g_func, x0, y0, g_const, l_const)

        output = BytesIO()
        fig.savefig(output, format='png')

        response = make_response(output.getvalue())
        response.mimetype = 'image/png'

        return response


def get_img(form: RungeKuttaPendulumForm):
    return RungeKutta.get_img(
        form.f.data,
        form.left_bound.data,
        form.right_bound.data,
        form.N.data,
        form.w.data,
        form.h.data,
        form.g.data,
        form.x0.data,
        form.y0.data,
        form.g_const.data,
        form.l_const.data,
    )

def get_coords(form: RungeKuttaPendulumForm):
    return RungeKutta.get_coords(
        form.f.data,
        form.left_bound.data,
        form.right_bound.data,
        form.N.data,
        form.w.data,
        form.h.data,
        form.g.data,
        form.x0.data,
        form.y0.data,
        form.g_const.data,
        form.l_const.data,
    )

methods = {
    'img': get_img,
    'coords': get_coords,
}