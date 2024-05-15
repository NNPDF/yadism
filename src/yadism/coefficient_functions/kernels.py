"""Coefficient function kernels.

Kernels are a combination of the coupling structure (which parton with which weight)
and the respective 'raw' mathematical coefficient function.
"""

import copy
import importlib
from numbers import Number

import numpy as np
from eko import basis_rotation as br


def import_local(kind, process, sibling):
    """Import the suitable subpackage with the actual partonic channel implementation.

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
    """Combination of partons with their weights and their mathematical expression in this channel.

    Parameters
    ----------
    partons : dict
        mapping pid -> weight
    coeff : PartonicChannel
        mathematical expression
    max_order : int
        if given, silence above this order
    min_order : int
        if given, silence below this order
    """

    def __init__(self, partons, coeff, max_order=None, min_order=None):
        self.partons = partons
        self.coeff = coeff
        self.max_order = max_order
        self.min_order = min_order

    def has_order(self, order):
        """Is current order active.

        Parameters
        ----------
        order : int
            order

        Returns
        -------
        bool :
            is active?
        """
        if self.min_order and order < self.min_order:
            return False
        if self.max_order and order > self.max_order:
            return False
        return True

    @property
    def channel(self):
        """Abstract classification in physical channels."""
        cls = str(type(self.coeff)).split("'")[1].split(".")[-1]

        # TODO: remove AsyQuark for AsyNonSinglet
        if "NonSinglet" in cls or "Quark" in cls:
            return "non-singlet"
        elif "Singlet" in cls:
            return "singlet"
        elif "Gluon" in cls:
            return "gluon"
        elif "Valence" in cls:
            return "valence"
        elif any(
            [x in cls for x in ["Intrinsic", "Splus", "Sminus", "Rplus", "Rminus"]]
        ):
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
        return self.__class__(
            partons, copy.copy(self.coeff), self.max_order, self.min_order
        )


def cc_weights(coupling_constants, Q2, cc_mask, nf, is_pv):
    """Collect the weights of the partons.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    Q2 : float
        W virtuality
    cc_mask : str
        participating flavors on the CKM matrix
    nf : int
        number of light flavors
    is_pv: bool
        True if observable violates parity conservation

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
            weights["ns"][sign * q] = w if not is_pv else sign * w
        # but it contributes to the average
        tot_ch_sq += w
    # gluon coupling = charge sum
    if rest == 0 and is_pv:
        tot_ch_sq *= -1
    weights["g"][21] = tot_ch_sq / norm / 2
    # add singlet
    for q in weights["ns"]:
        weights["s"][q] = tot_ch_sq / norm / 2
        weights["s"][-q] = tot_ch_sq / norm / 2
    return weights


def cc_weights_even(coupling_constants, Q2, cc_mask, nf, is_pv):
    """Collect the weights of the partons.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    Q2 : float
        W virtuality
    cc_mask : str
        participating flavors on the CKM matrix
    nf : int
        number of light flavors
    is_pv: bool
        True if observable violates parity conservation

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
            weights["ns"][sign * q] = w / 2 * (1 if not is_pv else sign)
            weights["ns"][-sign * q] = w / 2 * (1 if not is_pv else sign)
        # but it contributes to the average
        tot_ch_sq += w
    # gluon coupling = charge sum
    weights["g"][21] = tot_ch_sq / norm / 2
    # add singlet
    for q in range(1, nf + 1):
        weights["s"][q] = tot_ch_sq / norm / 2
        weights["s"][-q] = tot_ch_sq / norm / 2
    return weights


def cc_weights_odd(coupling_constants, Q2, cc_mask, nf, is_pv):
    """Collect the weights of the partons.

    Parameters
    ----------
    coupling_constants : CouplingConstants
        manager for coupling constants
    Q2 : float
        W virtuality
    cc_mask : str
        participating flavors on the CKM matrix
    nf : int
        number of light flavors
    is_pv: bool
        True if observable violates parity conservation

    Returns
    -------
    weights : dict
        mapping pid -> weight for q and g channel
    """
    weights = {"ns": {}, "v": {}}
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
            weights["ns"][sign * q] = w / 2 * (1 if not is_pv else sign)
            weights["ns"][-sign * q] = -w / 2 * (1 if not is_pv else sign)
        tot_ch_sq += w
    # add valence, here there is no need to distinguish up and down.
    for q in range(1, nf + 1):
        weights["v"][q] = tot_ch_sq / norm / 2
        weights["v"][-q] = -tot_ch_sq / norm / 2
    return weights


def generate_single_flavor_light(esf, nf, ihq):
    """Add a light-like contribution for a single quark flavor.

    The linear dependency to the electric charge is introduce by multiplying
    and diving by nf. The multiplication is *implicit* inside the coefficient function,
    the division is *explicit* made here.

    Parameters
    ----------
    esf : EvaluatedStructureFunction
        kinematic point
    nf : int
        number of light flavors
    ihq : int
        quark flavor to activate

    Returns
    -------
    elems : list(yadism.kernels.Kernel)
        list of elements
    """
    kind = esf.info.obs_name.kind
    is_pv = esf.info.obs_name.is_parity_violating
    light_cfs = import_local(
        kind, esf.process, ".".join(__name__.split(".")[:-1] + ["light", ""])
    )
    if esf.process == "CC":
        w_even = cc_weights_even(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[ihq - 1],
            nf,
            is_pv,
        )
        ns_even = Kernel(w_even["ns"], light_cfs.NonSingletEven(esf, nf))
        w_odd = cc_weights_odd(
            esf.info.coupling_constants,
            esf.Q2,
            br.quark_names[ihq - 1],
            nf,
            is_pv,
        )
        ns_odd = Kernel(w_odd["ns"], light_cfs.NonSingletOdd(esf, nf))

        if is_pv:
            v = Kernel(
                {k: np.sign(k) * c / (nf) for k, c in w_odd["s"].items()},
                light_cfs.Valence(esf, nf),
            )
            return (ns_even, ns_odd, v)
        g = Kernel({21: w_even["g"][21] / (nf)}, light_cfs.Gluon(esf, nf))
        s = Kernel(
            {k: v / (nf) for k, v in w_even["s"].items()}, light_cfs.Singlet(esf, nf)
        )
        return (ns_even, g, s, ns_odd)

    # NC
    if is_pv:
        w = esf.info.coupling_constants.get_weight(
            ihq, esf.Q2, "VA"
        ) + esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AV")
    else:
        w = esf.info.coupling_constants.get_weight(
            ihq, esf.Q2, "VV"
        ) + esf.info.coupling_constants.get_weight(ihq, esf.Q2, "AA")

    ns_partons = {}
    ns_partons[ihq] = w
    ns_partons[-ihq] = w if not is_pv else -w
    ch_av = w / nf  # omitting again *2/2

    # all quarks from 1 up to and including nf for the singlet and valence
    pids = range(1, nf + 1)
    if is_pv:
        v_partons = {q: np.sign(q) * ch_av for q in [*pids, *(-q for q in pids)]}
        return (
            Kernel(ns_partons, light_cfs.NonSinglet(esf, nf)),
            Kernel(v_partons, light_cfs.Valence(esf, nf)),
        )

    s_partons = {q: ch_av for q in [*pids, *(-q for q in pids)]}
    kernels_list = [
        Kernel(ns_partons, light_cfs.NonSinglet(esf, nf)),
        Kernel({21: ch_av}, light_cfs.Gluon(esf, nf)),
        Kernel(s_partons, light_cfs.Singlet(esf, nf)),
    ]

    if esf.info.theory["pto"] == 3:
        w = esf.info.coupling_constants.get_fl11_weight(
            ihq, esf.Q2, nf, "VV"
        ) + esf.info.coupling_constants.get_fl11_weight(ihq, esf.Q2, nf, "AA")
        quark_partons = {}
        quark_partons[ihq] = w
        quark_partons[-ihq] = w
        ch_av = w / nf
        kernels_list.extend(
            [
                Kernel(quark_partons, light_cfs.QuarkFL11(esf, nf)),
                Kernel({21: ch_av}, light_cfs.GluonFL11(esf, nf)),
            ]
        )
    return kernels_list
