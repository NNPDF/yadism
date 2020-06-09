# -*- coding: utf-8 -*-


class CouplingConstants:
    """
        Defines the coupling constants between the QCD particles and the EW particles
    """

    def __init__(self):
        # electric charge
        self.electric_charge = {21: 0}
        for q in range(7):
            self.electric_charge[q] = 2 / 3 if q % 2 == 0 else -1 / 3
            self.electric_charge[-q] = -self.electric_charge[q]
        self.electric_charge_sq = {
            pid: e ** 2 for pid, e in self.electric_charge.items()
        }

    @classmethod
    def from_theory(cls, _theory):
        """
            Creates the object from the theory dictionary

            Parameters
            ----------
                theory : dict
                    theory dictionary

            Returns
            -------
                o : CouplingConstants
                    created object
        """
        o = cls()
        return o
