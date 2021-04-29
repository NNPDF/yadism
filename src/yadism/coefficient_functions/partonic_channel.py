# -*- coding: utf-8 -*-


class PartonicChannel(dict):
    """
    Container of partonic coefficient functions

    Parameters
    ----------
        ESF : yadism.structure_function.esf.EvaluatedStructureFunction
            parent ESF
    """

    def __init__(self, ESF):
        super().__init__()
        self.ESF = ESF
        # default coeff functions to 0
        self[(0, 0, 0, 0)] = self.decorator(self.LO)
        self[(1, 0, 0, 0)] = self.decorator(self.NLO)
        self[(1, 0, 0, 1)] = self.decorator(self.NLO_fact)

    def convolution_point(self):
        """
        Convolution point
        """
        return self.ESF.x  # pylint: disable=protected-access

    def decorator(self, f):
        """
        Deactivate preprocessing

        Parameters
        ----------
            f : callable
                input

        Returns
        -------
            f : callable
                output
        """
        return f

    @staticmethod
    def LO():
        return None

    @staticmethod
    def NLO():
        return None

    @staticmethod
    def NLO_fact():
        return None


class EmptyPartonicChannel(PartonicChannel):
    def __init__(self, *args, **_kwargs):
        super().__init__(*args)
