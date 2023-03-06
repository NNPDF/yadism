import numpy as np
from eko.mellin import Path
from ekore.harmonics import compute_cache
from ekore.operator_matrix_elements.unpolarized.space_like import as2
from numpy.testing import assert_allclose
from scipy.integrate import quad


from test_pc_general import MockESF
from yadism.coefficient_functions.fonll.partonic_channel import (
    PdfMatchingNNLLNonSinglet,
)

nf = 4
mhq = 1.51

# a simple test function  and its mellin transform
def f(x):
    return x * (1 - x)

def mellin_f(n):
    return 1 / (2 + 3 * n + n**2)

# x-space convolution
def yad_convolute(x, q):
    esf = MockESF(x, q**2)
    match = PdfMatchingNNLLNonSinglet(esf, nf, m2hq=q**2).NNLO()
    loc = match.loc(x, match.args["loc"]) * f(x)
    sing = quad(
        lambda z: match.sing(z, match.args["sing"]) * (f(x / z) / z - f(x)),
        x,
        1,
    )[0]
    return sing + loc

# n-space convolution
def inverse_mellin(x):
    def quad_ker_talbot(u, func):
        path = Path(u, np.log(x), True)
        sx = compute_cache(path.n, 3, True)
        sx = [np.array(s) for s in sx]
        integrand = path.prefactor * x ** (-path.n) * path.jac
        gamma = func(path.n, sx, L=0) * mellin_f(path.n)
        return np.real(gamma * integrand)

    return quad(
        lambda u: quad_ker_talbot(u, as2.A_qq_ns),
        0.5,
        1.0,
        epsabs=1e-12,
        epsrel=1e-6,
        limit=200,
        full_output=1,
    )[0]


class Test_Matching_qq:
    xs = [0.0001, 0.001, 0.01, 0.1, 0.2, 0.456, 0.7]
    Qs = [5, 10, 20]

    def test_nnlo(self):
        my = []
        eko = []
        for q in self.Qs:
            for x in self.xs:
                my.append(yad_convolute(x, q))
                eko.append(inverse_mellin(x))
        assert_allclose(my, eko)
