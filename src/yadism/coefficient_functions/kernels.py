# -*- coding: utf-8 -*-
import copy
import importlib
from numbers import Number


def import_local(kind, process, sibling):
    """
    Import the suitable subpackage with the actual partonic channel implementation.

    Parameters
    ----------
        kind : str
            structure function kind
        process : str
            DIS process type: "EM","NC","CC"
        sibling : str
            relative parent to import from

    Returns
    -------
        module : module
            module
    """
    kind = kind.lower()
    process = process.lower()
    if process == "em":
        process = "nc"
    parent = ".".join(sibling.split(".")[:-1])
    return importlib.import_module(f".{kind}_{process}", parent)


class Kernel:
    """
    Combination of partons with their weights and their mathematical expression in this channel.

    Parameters
    ----------
        partons : dict
            mapping pid -> weight
        coeff : PartonicChannel
            mathematical expression
    """

    def __init__(self, partons, coeff):
        self.partons = partons
        self.coeff = coeff

    @property
    def channel(self):
        cls = str(type(self.coeff)).split("'")[1].split(".")[-1]

        # TODO: remove AsyQuark for AsyNonSinglet
        if "NonSinglet" in cls or "Quark" in cls:
            return "non-singlet"
        elif "Singlet" in cls:
            return "singlet"
        elif "Gluon" in cls:
            return "gluon"
        elif any([x in cls for x in ["Splus", "Sminus", "Rplus", "Rminus"]]):
            return "intrinsic"
        else:
            raise ValueError(f"Class '{cls}' does not correspond to a known channel")

    def __repr__(self):
        return repr({"partons": self.partons, "coeff": self.coeff})

    def __neg__(self):
        return self.__rmul__(-1)

    def __mul__(self, f):
        return self.__rmul__(f)

    def __rmul__(self, f):
        if not isinstance(f, Number):
            raise ValueError("Can only multiply numbers")
        partons = {k: f * v for k, v in self.partons.items()}
        return self.__class__(partons, copy.copy(self.coeff))


flavors = "duscbt"


def cc_weights(coupling_constants, Q2, kind, cc_mask, nf):
    """
    Collect the weights of the partons.

    Parameters
    ----------
        coupling_constants : CouplingConstants
            manager for coupling constants
        Q2 : float
            W virtuality
        kind : str
            structure function kind
        cc_mask : str
            participating flavors on the CKM matrix
        nf : int
            number of light flavors

    Returns
    -------
        weights : dict
            mapping pid -> weight for q and g channel
    """
    weights = {"ns": {}, "g": {}, "s": {}}
    # determine couplings
    projectile_pid = coupling_constants.obs_config["projectilePID"]
    if projectile_pid in [-11, 12]:
        rest = 1
    else:
        rest = 0
    # quark couplings
    tot_ch_sq = 0
    norm = len(cc_mask)
    # iterate: include the heavy quark itself, since it can run in the singlet sector diagrams
    for q in range(1, min(nf + 2, 6 + 1)):
        sign = 1 if q % 2 == rest else -1
        w = coupling_constants.get_weight(q, Q2, None, cc_mask=cc_mask)
        # the heavy quark can not be in the input
        # NOTE: intrinsic abuse this statement with nf -> nf + 1
        if q <= nf:
            # @F3-sign@
            weights["ns"][sign * q] = w if kind != "F3" else sign * w
        # but it contributes to the average
        tot_ch_sq += w
    # gluon coupling = charge sum
    if rest == 0 and kind == "F3":
        tot_ch_sq *= -1
    weights["g"][21] = tot_ch_sq / norm / 2
    # add singlet
    for q in weights["ns"]:
        weights["s"][q] = tot_ch_sq / norm / 2
        weights["s"][-q] = tot_ch_sq / norm / 2
    return weights
