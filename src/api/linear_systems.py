from flask import make_response, send_from_directory

import numpy as np
import json

def get_generated_linear_system(n):
    b = np.array([i for i in range(1, n + 1)], dtype='float64').T
    a = np.array(
        [
            [-j for j in range(1, i)] + [0 if i > 1 else 1] + [j for j in range(i + 1, n + 1)] 
            for i in range(1, n + 1)
        ],
        dtype='float64'
    )
    return (a, b)


class Jacobi:
    @classmethod
    def get_answer(cls, linear_system):
        a = linear_system[0]
        b = linear_system[1]
        n = b.shape[0]
        D = np.diag(np.diag(a))
        Dinv = np.linalg.inv(D)
        
        B = Dinv @ (D - A)
        g = Dinv @ b

        x = np.zeroes(n)
        for i in range(100):
            x = B @ x + g
        return x

class Gaussian:
    @classmethod
    def get_answer(cls, linear_system):
        a = linear_system[0]
        b = linear_system[1]
        n = b.shape[0]
        ab = np.column_stack((a, b))

        for i in range(n):
            ab[i] /= ab[i][i]
            for j in range(i + 1, n):
                ab[j] -= ab[j][i] * ab[i]
        a_changed = ab[:, : n ]
        ans = np.zeros((n,))
        for i in range(n - 1, -1, -1):
            ans[i] = ab[i][n] - sum(ans * a_changed[i])

        err = sum(np.abs((a @ ans) - b))
        return dict(ans=ans.tolist(), error=err)


def get_gaussian_solution(form):
    system = get_generated_linear_system(form.n.data)
    result = Gaussian.get_answer(system)
    return json.dumps(result)

def get_jakobi_solution(form):
    system = get_generated_linear_system(form.n.data)
    try:
        result = Jacobi.get_answer(system)
        return json.dumps(result)
    except np.linalg.linalg.LinAlgError:
        return json.dumps(dict(error_occured="Unable to apply Jacobi method"))

methods = {
    'gaussian': get_gaussian_solution,
    'jacobi': get_jakobi_solution
}