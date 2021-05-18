# -*- coding: utf-8 -*-

import numbers

import numpy as np


class ESFResult:
    """
    Represents the output tensor for a single kinematic point

    Parameters
    ----------
        x : float
            Bjorken x
        Q2 : float
            virtuality of the exchanged boson
    """

    def __init__(self, x, Q2, nf, orders=None):
        self.x = x
        self.Q2 = Q2
        self.nf = nf
        self.orders = {} if orders is None else orders

    @classmethod
    def from_document(cls, raw):
        """
        Recover element from a raw dictionary

        Parameters
        ----------
            raw : dict
                raw dictionary

        Returns
        -------
            new_output : cls
                object representation
        """
        new_output = cls(raw["x"], raw["Q2"], raw["nf"])
        for e in raw["orders"]:
            new_output.orders[tuple(e["order"])] = (
                np.array(e["values"]),
                np.array(e["errors"]),
            )
        return new_output

    def apply_pdf(self, lhapdf_like, pids, xgrid, alpha_s, alpha_qed, sv):
        r"""
        Compute the observable for the given PDF.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
                and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)
            pids : list(int)
                list of pids
            xgrid : list(float)
                interpolation grid
            xiF : float
                factorization scale ration :math:`\mu_F^2 = Q^2 \xi_F^2` - beware the square!

        Returns
        -------
            res : dict
                output dictionary with x, Q2, result and error
        """
        if not isinstance(self.Q2, numbers.Number):
            raise ValueError("Q2 is not set!")

        # factorization scale
        if sv is not None and "xiF" in sv:
            muF2 = self.Q2 * sv["xiF"] ** 2
        else:
            muF2 = self.Q2
        pdfs = np.zeros((len(pids), len(xgrid)))
        for j, pid in enumerate(pids):
            if not lhapdf_like.hasFlavor(pid):
                continue
            pdfs[j] = np.array([lhapdf_like.xfxQ2(pid, z, muF2) / z for z in xgrid])

        # prepare convolutions
        raw = []
        fact_sv_list = []
        for o, (v, e) in self.orders.items():
            res_o, err_o = np.einsum("aj,aj", v, pdfs), np.einsum("aj,aj", e, pdfs)
            raw.append((res_o, err_o))
            # apply factorization scale variations matrices
            if sv is not None and "xiF" in sv:
                for ((alphas_power, lnf_power), src), mat in sv[
                    "fact_matrices"
                ].items():
                    if alphas_power != o:
                        continue
                    prefactor = (-np.log(sv["xiF"] ** 2)) ** lnf_power
                    res_o += prefactor * np.einsum("aj,aj", mat @ raw[src][0], pdfs)
                    err_o += prefactor * np.einsum("aj,aj", mat @ raw[src][1], pdfs)
            fact_sv_list.append((res_o, err_o))
        # apply ren/fact scale variations
        fact_ren_sv_list = fact_sv_list
        if sv is not None and "fact_to_ren_scale_ratio" in sv:
            for (
                (alphas_power, lnrf_power),
                src,
            ), nf_coeffs in sv["fact_to_ren_prefactors"].items():
                prefactor = (nf_coeffs @ (self.nf ** np.arange(len(nf_coeffs)))) * (
                    np.log(sv["fact_to_ren_scale_ratio"] ** 2)
                ) ** lnrf_power
                fact_ren_sv_list[alphas_power][0] += prefactor * fact_sv_list[src][0]
                fact_ren_sv_list[alphas_power][1] += prefactor * fact_sv_list[src][1]

        # join elements
        res = 0
        err = 0
        if sv is not None:
            xiF = sv.get("xiF", 1.0)
            fact_to_ren_scale_ratio = sv.get("fact_to_ren_scale_ratio", 1.0)
            xiR = xiF / fact_to_ren_scale_ratio
        else:
            xiR = 1.0
        my_alpha_s = alpha_s(np.sqrt(self.Q2) * xiR) / (4 * np.pi)
        for o, (v, e) in enumerate(fact_sv_list):
            prefactor = (my_alpha_s) ** o
            res += prefactor * v
            err += prefactor * e

        return dict(x=self.x, Q2=self.Q2, result=res, error=err)

    def get_raw(self):
        """
        Returns the raw data ready for serialization.

        Returns
        -------
            out : dict
                output dictionary
        """
        d = dict(x=self.x, Q2=self.Q2, nf=self.nf, orders=[])
        for o, (v, e) in self.orders.items():
            d["orders"].append(
                dict(order=list(o), values=v.tolist(), errors=e.tolist())
            )
        return d

    def __add__(self, other):
        r = ESFResult(self.x, self.Q2, self.nf)
        for o, (v, e) in self.orders.items():
            if o in other.orders:  # add the common stuff
                r.orders[o] = (v + other.orders[o][0], e + other.orders[o][1])
            else:  # add my stuff
                r.orders[o] = (v, e)
        for o, (v, e) in other.orders.items():
            if o in self.orders:
                continue
            # add his stuff
            r.orders[o] = (v, e)
        return r

    def __sub__(self, other):
        return self.__add__(-other)

    def __neg__(self):
        return self.__mul__(-1.0)

    def __mul__(self, other):
        r = ESFResult(self.x, self.Q2, self.nf)
        try:
            val = other[0]
            err = other[1]
        except TypeError:
            val = other
            err = 0
        for o, (v, e) in self.orders.items():
            r.orders[o] = (val * v, val * e + err * v)
        return r

    def __rmul__(self, other):
        return self.__mul__(other)


class EXSResult(ESFResult):
    def __init__(self, x, Q2, y, nf, orders=None):
        super().__init__(x, Q2, nf, orders)
        self.y = y

    @classmethod
    def from_document(cls, raw):
        sup = super().from_document(raw)
        return cls(sup.x, sup.Q2, raw["y"], sup.nf, sup.orders)

    def get_raw(self):
        d = super().get_raw()
        d["y"] = self.y
        return d
