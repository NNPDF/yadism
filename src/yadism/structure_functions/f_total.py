# -*- coding: utf-8 -*-


from . import esf
from . import esf_result


class EvaluatedStructureFunctionFtotal(esf.EvaluatedStructureFunction):
    """
        Complete structure function

        Parameters
        ----------
            SF : StructureFunction
                the parent :py:class:`StructureFunction` instance
            kinematics : dict
                the specific kinematic point as a dict with two elements ('x', 'Q2')
    """

    def __init__(self, SF, kinematics: dict):
        super(EvaluatedStructureFunctionFtotal, self).__init__(SF, kinematics)
        self._sf_kind = self._SF.name[:2]

    def get_result(self):
        """
            Combine all other ESFs together

            Returns
            -------
                res : ESFResult
                    joined elements
        """
        # final object
        res = esf_result.ESFResult(self._x, self._Q2)
        kin = {"x": self._x, "Q2": self._Q2}
        # light component
        res_light = self._SF.get_esf(
            self._sf_kind + "light", kin, use_raw=False
        ).get_result()
        # charm component
        res_charm = self._SF.get_esf(
            self._sf_kind + "charm", kin, use_raw=False
        ).get_result()
        # bottom component
        res_bottom = self._SF.get_esf(
            self._sf_kind + "bottom", kin, use_raw=False
        ).get_result()
        # top component
        res_top = self._SF.get_esf(
            self._sf_kind + "top", kin, use_raw=False
        ).get_result()
        # rename and add
        for res_sub, suffix in [
            (res_light, "light"),
            (res_charm, "charm"),
            (res_bottom, "bottom"),
            (res_top, "top"),
        ]:
            for k in res_sub.values:
                res.values[k + suffix] = res_sub.values[k]
                res.errors[k + suffix] = res_sub.errors[k]
                res.weights[k + suffix] = res_sub.weights[k]
        return res

    def _compute_weights(self):
        raise NotImplementedError(
            f"{self._sf_kind}total: this method should never be called!"
        )

    def quark_0(self):
        raise NotImplementedError(
            f"{self._sf_kind}total: this method should never be called!"
        )

    def quark_1(self):
        raise NotImplementedError(
            f"{self._sf_kind}total: this method should never be called!"
        )

    def quark_1_fact(self):
        raise NotImplementedError(
            f"{self._sf_kind}total: this method should never be called!"
        )

    def gluon_1(self):
        raise NotImplementedError(
            f"{self._sf_kind}total: this method should never be called!"
        )

    def gluon_1_fact(self):
        raise NotImplementedError(
            f"{self._sf_kind}total: this method should never be called!"
        )
