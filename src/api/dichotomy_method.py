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

    @staticmethod
    def get_val(f, x):
        names = DichotomyMethod.ALLOWED_FUNCTIONS.copy()
        names['x'] = x

        return eval(f, {'__builtins__': None}, names)
    
    @staticmethod
    def get_answer(f, a, b, eps):
        import logging
        logging.log(logging.CRITICAL, str([f, a, b, eps]))
        
        if eps < 1e-9:
            return "Error. Epsilon must be greater than 0.000'000'001"
        if a >= b:
            return "Error. A must be less than B"
        if DichotomyMethod.get_val(f, a) * DichotomyMethod.get_val(f, b) > 0:
            logging.critical(DichotomyMethod.get_val(f, a))
            logging.critical(DichotomyMethod.get_val(f, b))
            
            return "Error. f(a) * f(b) must be not greater than zero."
        while a + eps < b:
            mid = (a + b) / 2
            if DichotomyMethod.get_val(f, a) * DichotomyMethod.get_val(f, mid) <= 0:
                b = mid
            else:
                a = mid
        return "%.9f" % ((a + b) / 2)


def get_img(form):
    return ""

def get_answer(form):
    return DichotomyMethod.get_answer(form.f.data, form.left_bound.data, form.right_bound.data, form.eps.data)
    


methods = {
    'img': get_img,
    'ans': get_answer
}