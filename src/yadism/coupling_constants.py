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

        # 3rd component of weak isospin ---------------------------------------
        # QCD particles
        self.weak_isospin_3 = {21: 0}
        for q in range(1, 7):
            self.weak_isospin_3[q] = 1 / 2 if q % 2 == 0 else -1 / 2  # u if stmt else d
        # leptons: 11 = e-(!)
        for pid in [11, 13, 15]:
            self.weak_isospin_3[pid] = -1 / 2
        # neutrinos
        for pid in [12, 14, 16]:
            self.weak_isospin_3[pid] = 1 / 2

    def _get_vectorial_coupling(self, pid):
        """Combine the vectorial coupling from electric and weak charges"""
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
        # for quarks only the flavor does matter
        pid = abs(pid)
        # keep in mind that for the projectile we *do* care about sign
        projectile_pid = self.obs_config["projectilePID"]
        eq = self.electric_charge[pid]
        # axial coupling of the photon to the quark is not there of course
        if quark_coupling_type == "A":
            eq = 0
        w_phph = (self.electric_charge[abs(projectile_pid)] ** 2) * (eq ** 2)
        # pure photon exchane
        if self.obs_config["process"] == "EM":
            return w_phph
        # allow Z to be mixed in
        if self.obs_config["process"] == "NC":
            # load coupling
            projectile_v = self._get_vectorial_coupling(abs(projectile_pid))
            projectile_a = self.weak_isospin_3[abs(projectile_pid)]
            gqv = self._get_vectorial_coupling(pid)
            gqa = self.weak_isospin_3[pid]
            # load proper polarization definition
            pol = self.obs_config["polarization"]
            if (projectile_pid % 2 == 1 and projectile_pid > 0) or (
                projectile_pid % 2 == 0 and projectile_pid < 0
            ):
                pol *= -1
            eta_phZ = (
                Q2
                / (self.theory_config["MZ2"] + Q2)
                / (
                    4.0
                    * self.theory_config["sin2theta_weak"]
                    * (1.0 - self.theory_config["sin2theta_weak"])
                )
            )
            eta_phZ /= 1 - self.obs_config["propagatorCorrection"]
            # photon-Z interference
            w_phZ = (
                2
                * self.electric_charge[abs(projectile_pid)]
                * (projectile_v + pol * projectile_a)
                * eta_phZ
                * eq
                * gqv
            )
            # in heavy quark structure functions the two coefficient functions for the
            # vectorial and axial-vectorial coupling are NOT the same (unlinke in the massless case)
            g2q = gqv ** 2 + gqa ** 2
            if quark_coupling_type == "V":
                g2q = gqv ** 2
            elif quark_coupling_type == "A":
                g2q = gqa ** 2
            # true Z contributions
            w_ZZ = (
                (
                    projectile_v ** 2
                    + projectile_a ** 2
                    + 2.0 * pol * projectile_v * projectile_a
                )
                * (eta_phZ ** 2)
                * g2q
            )
            return w_phph + w_phZ + w_ZZ
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
        # map projectile to PID
        projectile = observables.get("ProjectileDIS", "electron")
        projectile_pids = {
            "electron": 11,
            "positron": -11,
            "neutrino": 12,
            "antineutrino": -12,
        }
        if projectile not in projectile_pids:
            raise ValueError(f"Unkown projectile {projectile}")
        obs_config = {
            "process": observables.get("prDIS", "EM"),
            "projectilePID": projectile_pids[projectile],
            "polarization": observables.get("PolarizationDIS", 0),
            "propagatorCorrection": observables.get("PropagatorCorrection", 0),
        }
        o = cls(theory_config, obs_config)
        return o
