import numpy as np
from eko.mellin import Path
from ekore.harmonics import cache
from ekore.operator_matrix_elements.polarized.space_like import as2
from numpy.testing import assert_allclose
from scipy.integrate import quad
from test_pc_general import MockESF

from yadism.coefficient_functions.fonll.g1_nc import (
    PdfMatchingLLNonSinglet,
    PdfMatchingNLLNonSinglet,
    PdfMatchingNNLLNonSinglet,
)

nf = 4
mhq = 1.51


# a simple test function  and its mellin transform
def f(_x):
    return 1


def mellin_f(n):
    return 1 / n


# x-space convolution
def yad_convolute(x, q):
    esf = MockESF(x, q**2)
    result = 0
    for matchingfunc in [
        PdfMatchingLLNonSinglet,
        PdfMatchingNLLNonSinglet,
        PdfMatchingNNLLNonSinglet,
    ]:
        match = matchingfunc(esf, nf, m2hq=mhq**2).NNLO()
        loc = match.loc(x, match.args["loc"]) * f(x)
        sing = quad(
            lambda z: match.sing(z, match.args["sing"]) * (f(x / z) / z - f(x)),
            x,
            1,
        )[0]
        reg = 0
        if match.reg is not None:
            reg = quad(
                lambda z: match.reg(z, match.args["reg"]) * f(x / z) / z,
                x,
                1,
            )[0]
        result += sing + loc + reg
    return result


# n-space convolution
def inverse_mellin(x, q):
    def quad_ker_talbot(u):
        path = Path(u, np.log(x), True)
        sx_cache = cache.reset()
        integrand = path.prefactor * x ** (-path.n) * path.jac
        gamma = as2.A_qq_ns(path.n, sx_cache, L=np.log(q**2 / mhq**2)) * mellin_f(
            path.n
        )
        return np.real(gamma * integrand)

    return quad(
        lambda u: quad_ker_talbot(u),
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
                eko.append(inverse_mellin(x, q))
        assert_allclose(my, eko)
