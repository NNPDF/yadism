# -*- coding: utf-8 -*-


def rsl_from_distr_coeffs(regular, delta, *coeffs):
    def singular(z, coeffs=coeffs):
        log_ = np.log(1 - z)
        res = 0
        for k, coeff in enumerate(coeffs):
            res += coeff * 1 / (1 - z) * log_ ** k
        return res

    def local(x, coeffs=coeffs):
        log_ = np.log(1 - x)
        res = 0
        for k, coeff in enumerate(coeffs):
            res += coeff * log_ ** (k + 1) / (k + 1)
        return res + delta

    return regular, singular, local
