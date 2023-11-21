def W2(x, Q2, MP=0.0):
    """Mass squared :math:`W^2` of the proton-boson system.

    In particular, it is the mass squared of the system X recoiling against the
    scattered lepton :cite:`Zyla:2020zbs`.

    Parameters
    ----------
    x: float
        Bjorken x
    Q2: float
        photon virtuality
    MP: float
        mass of the proton (default: ``0.``)

    Returns
    -------
    float
        :math:`W^2` value computed

    """
    return MP**2 + Q2 * (1 - x) / x
