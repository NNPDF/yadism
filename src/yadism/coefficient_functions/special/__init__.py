import numba as nb
import numpy as np

from .zeta import zeta2, zeta3


@nb.njit("f8(f8)", cache=True)
def li2(X):
    """
    Reimplementation of DDILOG (C332) from CERNlib :cite:`cernlib`.

    Note
    ----
    This is the dilog (:math:`Li_2(x)`) and *not* the Spence's function
    (:data:`scipy.special.spence`).

    Parameters
    ----------
    X : float
        argument of :math:`Li_2(x)`

    Returns
    -------
    float
        :math:`Li_2(x)`

    """
    # fmt: off
    Z1 = 1
    HF = Z1/2
    PI = 3.14159265358979324
    PI3 = PI**2/3
    PI6 = PI**2/6
    PI12 = PI**2/12

    C = np.array([
        +0.42996693560813697,
        +0.40975987533077105,
        -0.01858843665014592,
        +0.00145751084062268,
        -0.00014304184442340,
        +0.00001588415541880,
        -0.00000190784959387,
        +0.00000024195180854,
        -0.00000003193341274,
        +0.00000000434545063,
        -0.00000000060578480,
        +0.00000000008612098,
        -0.00000000001244332,
        +0.00000000000182256,
        -0.00000000000027007,
        +0.00000000000004042,
        -0.00000000000000610,
        +0.00000000000000093,
        -0.00000000000000014,
        +0.00000000000000002,
    ])

    if X == 1:
        H=PI6
    elif X == -1:
        H=-PI12
    else:
        T=-X
        if T <= -2:
            Y=-1/(1+T)
            S=1
            A=-PI3+HF*(np.log(-T)**2-np.log(1+1/T)**2)
        elif T < -1:
            Y=-1-T
            S=-1
            A=np.log(-T)
            A=-PI6+A*(A+np.log(1+1/T))
        elif T <= -HF:
            Y=-(1+T)/T
            S=1
            A=np.log(-T)
            A=-PI6+A*(-HF*A+np.log(1+T))
        elif T < 0:
            Y=-T/(1+T)
            S=-1
            A=HF*np.log(1+T)**2
        elif T <= 1:
            Y=T
            S=1
            A=0
        else:
            Y=1/T
            S=-1
            A=PI6+HF*np.log(T)**2

        H=Y+Y-1
        ALFA=H+H
        B1=0
        B2=0
        for I in range(19, 0-1, -1):
            B0=C[I]+ALFA*B1-B2
            B2=B1
            B1=B0

        H=-(S*(B0-H*B2)+A)

    DDILOG=H
    # fmt: on

    return DDILOG


@nb.njit("f8(f8)", cache=True)
def s2(z):
    x = z

    lnx = np.log(x)
    ddilog = li2

    S2 = -2 * ddilog(-x) + lnx ** 2 / 2 - 2 * lnx * np.log(1 + x) - np.pi ** 2 / 6

    return S2
