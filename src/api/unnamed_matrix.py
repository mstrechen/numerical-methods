from flask import make_response, send_from_directory

import numpy as np
import json

class Function:
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

    def __init__(self, func_text):
        self.func_text = func_text

    def get(self, i, j):
        names = self.ALLOWED_FUNCTIONS.copy()
        names['i'] = i
        names['j'] = j
        return eval(self.func_text, {'__builtins__': None}, names)

class UnnamedMatrix:

    @staticmethod
    def PPOW(x, y):
        if x < 1e-14 and y < 1e-14:
            return 1
        return x**y
    
    @classmethod
    def get_unnamed_matrix(self, n, m, k, func):
        f = Function(func)
        x = [
            np.array([f.get(i, j) for j in range(1, m + 1)])
            for i in range(1, k + 1)
        ]
        GammaK = [
            [
                sum([self.PPOW(np.dot(x[i], x[j]), p) for p in range(n + 1) ])
                for j in range(k)
            ]
            for i in range(k)
        ]
        GammaK_inv = np.linalg.inv(np.array(GammaK))
        
        return dict(
            x=[val.tolist() for val in x],
            GammaK=GammaK,
            GammaKInv=GammaK_inv.tolist()
        )


def get_solution(form):
    n = form.n.data
    m = form.m.data
    k = form.k.data
    func = form.func.data
    return json.dumps(
        UnnamedMatrix.get_unnamed_matrix(n, m, k, func)
    )

methods = {
    'get': get_solution
}