# -*- coding: utf-8 -*-


from . import esf


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

    def get_result(self):
        """
            Combine all other ESFs together

            Returns
            -------
                res : ESFResult
                    joined elements
        """
        # final object
        kin = {"x": self._x, "Q2": self._Q2}
        # light component
        res_light = self._SF.get_esf(
            self._SF.obs_name.apply_flavor("light"), kin, use_raw=False
        ).get_result()
        # charm component
        res_charm = self._SF.get_esf(
            self._SF.obs_name.apply_flavor("charm"), kin, use_raw=False
        ).get_result()
        # bottom component
        res_bottom = self._SF.get_esf(
            self._SF.obs_name.apply_flavor("bottom"), kin, use_raw=False
        ).get_result()
        # top component
        res_top = self._SF.get_esf(
            self._SF.obs_name.apply_flavor("top"), kin, use_raw=False
        ).get_result()
        # rename and add
        return (
            res_light.suffix("_total_light")
            + res_charm.suffix("_total_charm")
            + res_bottom.suffix("_total_bottom")
            + res_top.suffix("_total_top")
        )

    @property
    def components(self):
        raise NotImplementedError(
            f"{self._SF.obs_name.name}: this method should never be called!"
        )

    def _compute_weights(self):
        raise NotImplementedError(
            f"{self._SF.obs_name.name}: this method should never be called!"
        )
