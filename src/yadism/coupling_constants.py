# -*- coding: utf-8 -*-


class CouplingConstants:
    """
        Defines the coupling constants between the QCD particles and the EW particles
    """

    def __init__(self, theory_config, obs_config):
        self.theory_config = theory_config
        self.obs_config = obs_config
        # electric charges ----------------------------------------------------
        # QCD particles
        self.electric_charge = {21: 0}
        for q in range(1, 7):
            self.electric_charge[q] = 2 / 3 if q % 2 == 0 else -1 / 3
        # leptons: 11 = e-(!)
        for pid in [11, 13, 15]:
            self.electric_charge[pid] = -1
        # neutrinos
        for pid in [12, 14, 16]:
            self.electric_charge[pid] = 0
        anti_electric = {}
        for pid in self.electric_charge:
            anti_electric[-pid] = -self.electric_charge[pid]
        self.electric_charge.update(anti_electric)

        # 3rd component of weak isospin ---------------------------------------
        # QCD particles
        self.weak_isospin_3 = {21: 0}
        for q in range(1, 7):
            self.weak_isospin_3[q] = -1 / 2 if q % 2 == 0 else 1 / 2
        # leptons: 11 = e-(!)
        for pid in [11, 13, 15]:
            self.weak_isospin_3[pid] = -1 / 2
        # neutrinos
        for pid in [12, 14, 16]:
            self.weak_isospin_3[pid] = 1 / 2
        anti_weak = {}
        for pid in self.weak_isospin_3:
            anti_weak[-pid] = self.weak_isospin_3[pid]
        self.weak_isospin_3.update(anti_weak)

    def _get_vectorial_coupling(self, pid):
        return (
            self.weak_isospin_3[pid]
            - 2.0 * self.electric_charge[pid] * self.theory_config["sin2theta_weak"]
        )

    def get_weight(self, pid, Q2, quark_coupling_type=None):
        """
            Compute the weight for the pid contributions to the structure function.

            Combine the charges, both on the leptonic side and the hadronic side, as well
            as propagator changes and/or corrections.

            Parameters
            ----------
                pid : int
                    particle identifier
                Q2 : float
                    DIS virtuality
                quark_coupling_type : str
                    flag to distinguish for heavy quarks between vectorial and axial-vectorial
                    coupling

            Returns
            -------
                w : float
                    weight
        """
        eq = self.electric_charge[pid]
        w = eq ** 2
        if self.obs_config["process"] == "EM":
            return w
        if self.obs_config["process"] == "NC":
            projectile_pid = self.obs_config["projectilePID"]
            projectile_v = self._get_vectorial_coupling(projectile_pid)
            projectile_a = self.weak_isospin_3[projectile_pid]
            gqv = self._get_vectorial_coupling(pid)
            gqa = self.weak_isospin_3[pid]
            # load proper polarization definition
            pol = self.obs_config["polarization"]
            if (projectile_pid % 2 == 1 and projectile_pid > 0) or (
                projectile_pid % 2 == 0 and projectile_pid < 0
            ):
                pol *= -1
            prop_swap = (
                Q2
                / (self.theory_config["MZ2"] + Q2)
                / (
                    4.0
                    * self.theory_config["sin2theta_weak"]
                    * (1.0 - self.theory_config["sin2theta_weak"])
                )
            )
            prop_swap /= 1 - self.obs_config["propagatorCorrection"]
            # photon-Z interference
            w -= 2 * (projectile_v  + pol * projectile_a) * prop_swap * eq * gqv
            # in heavy quark structure functions the two coefficient functions for the
            # vectorial and axial-vectorial coupling are NOT the same (unlinke in the massless case)
            g2q = gqv ** 2 + gqa ** 2
            if quark_coupling_type == "V":
                g2q = gqv ** 2
            elif quark_coupling_type == "A":
                g2q = gqa ** 2
            # true Z contributions
            w += (
                (
                    projectile_v ** 2
                    + projectile_a ** 2
                    + 2.0 * pol * projectile_v * projectile_a
                )
                * prop_swap ** 2
                * g2q
            )
            return w
        return 0

    @classmethod
    def from_dict(cls, theory, observables):
        """
            Creates the object from the theory dictionary

            Parameters
            ----------
                theory : dict
                    theory dictionary
                observables : dict
                    observables dictionary

            Returns
            -------
                o : CouplingConstants
                    created object
        """
        theory_config = {
            "MZ2": theory.get("MZ", 91.1876) ** 2,  # defaults to the PDG2020 value
            "sin2theta_weak": theory.get(
                "SIN2TW", 0.23121
            ),  # defaults to the PDG2020 value
        }
        # projectile = observables.get("ProjectileDIS", "electron")
        obs_config = {
            "process": observables.get("prDIS", "EM"),
            "projectilePID": 11,
            "polarization": observables.get("PolarizationDIS", 0),
            "propagatorCorrection": observables.get("PropagatorCorrection", 0),
        }
        o = cls(theory_config, obs_config)
        return o
