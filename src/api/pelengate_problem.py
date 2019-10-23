from flask import make_response, send_from_directory

from .forms import PelengateProblem

import matplotlib
import json

matplotlib.use('Agg')

import matplotlib.pyplot as plt

from io import StringIO, BytesIO

import numpy as np


class MatrixNewtonMethod:
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
        names = MatrixNewtonMethod.ALLOWED_FUNCTIONS.copy()
        names['x'] = x
        return eval(f, {'__builtins__': None}, names)

    @staticmethod
    def check_f_a_b(f, a, b):
        import logging
        logging.critical(f + "|" + str(a) + "-" + str(b) )
        if a >= b:
            return False
        try:
            MatrixNewtonMethod.get_val(f, a)
        except (NameError, SyntaxError):
            return False

        return True


    @classmethod
    def getdelta(cls, n, coefs, curx, cury):
        jacob_matrix = [
            [-2 * x + 2 * curx, -2 * y + 2 * cury]
            for x, y, r in coefs
        ]
        fvalues = [
            (x - curx) * (x - curx) + (y - cury) * (y - cury) - r * r
            for x, y, r in coefs
        ]

        # JrT * Jr * ck1 = JrT * Jr ck - JrT * r(ck)
        # ck1 = inv(JrT * Jr)(JrT * Jr * ck - JrT * r(ck))

        Jr = np.array(jacob_matrix)
        fvalues = np.array([fvalues]).T

        ckcur = np.array([[curx, cury]]).T
        cknew = np.linalg.pinv(Jr.T @ Jr) @ (Jr.T @ Jr @ ckcur - Jr.T @ fvalues)

        return cknew.T.ravel()

    @classmethod
    def get_answer_seq(cls, n, iters, xstart, ystart, coefs):
        res_x = [xstart]
        res_y = [ystart]
        curx, cury = xstart, ystart
        for i in range(iters):
            value = cls.getdelta(n, coefs, curx, cury)
            curx, cury = value[0], value[1]
            res_x.append(curx)
            res_y.append(cury)

        return res_x, res_y

    @classmethod
    def get_answer(cls, n, iters, xstart, ystart, coefs):
        return 'Hm...', 0

    @staticmethod
    def error_img():
        return send_from_directory('static/img', 'math-error.jpg')

    @staticmethod
    def draw_default_fig(w, h, values):
        fig = plt.figure(
            figsize=(w / MatrixNewtonMethod.DPI,
                     h / MatrixNewtonMethod.DPI), dpi=MatrixNewtonMethod.DPI * 4)

        graphic = fig.add_subplot(1, 1, 1)

        graphic.grid()
        minx = min(x - r for x, y, r in values) - 1
        maxx = max(x + r for x, y, r in values) + 1
        miny = min(y - r for x, y, r in values) - 1
        maxy = max(y + r for x, y, r in values) + 1

        graphic.set_xlim([minx, maxx])
        graphic.set_ylim([miny, maxy])

        for x, y, r in values:
            graphic.add_patch(plt.Circle((x, y), r, fill=False))

        return fig, graphic

    @classmethod
    def draw_graphic(cls, n, iters, xstart, ystart, coefs, w, h):
        fig, graphic = MatrixNewtonMethod.draw_default_fig(w, h, coefs)

        graphic.scatter([1, 2, 3], [0, 1, 2], color='g', zorder=1, alpha=0.3)
        X, Y = cls.get_answer_seq(n, iters, xstart, ystart, coefs)
        graphic.plot(X, Y, '-b', zorder=1)

        # X = np.linspace(a, b, w)
        # Y = MatrixNewtonMethod.get_val(f, X)
        #
        # graphic.plot(X, Y, 'b-', zorder=1)
        #
        # if tracing:
        #     res = MatrixNewtonMethod.get_answer_seq(f, lamb, a, b, x0, iter_count)
        #     res = np.array(res)
        #     resy = MatrixNewtonMethod.get_val(f, res)
        #     graphic.scatter(res, resy, color='g', zorder=4, alpha=0.3)
        #
        # sol = MatrixNewtonMethod.get_answer(f, lamb, a, b, x0, iter_count)[0]
        #
        # if type(sol) is not str:
        #     graphic.scatter([sol], [0], color='y', zorder=5)

        return fig

    @classmethod
    def get_img(cls, n, iters, xstart, ystart, coefs, w, h):

        fig = cls.draw_graphic(n, iters, xstart, ystart, coefs, w, h)

        output = BytesIO()
        fig.savefig(output, format='png')

        response = make_response(output.getvalue())
        response.mimetype = 'image/png'

        return response


def get_img(form: PelengateProblem):
    return MatrixNewtonMethod.get_img(
        form.N.data,
        form.iters.data,
        form.xstart.data,
        form.ystart.data,
        json.loads(form.coefs.data),
        form.w.data,
        form.h.data
    )


def get_answer(form: PelengateProblem):
    ans = MatrixNewtonMethod.get_answer(
        form.N.data,
        form.iters.data,
        form.xstart.data,
        form.ystart.data,
        json.loads(form.coefs.data)
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