# -*- coding: utf-8 -*-
import logging

import numpy as np

logger = logging.getLogger(__name__)


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
        self.log()

    def log(self):
        """Write current configuration to log"""
        logger.info(self.theory_config)
        logger.info(self.obs_config)

    def vectorial_coupling(self, pid):
        """Combine the vectorial coupling from electric and weak charges"""
        return (
            self.weak_isospin_3[pid]
            - 2.0 * self.electric_charge[pid] * self.theory_config["sin2theta_weak"]
        )

    def leptonic_coupling(self, mode, quark_coupling_type):
        """
        Computes the coupling of the boson to the lepton

        Parameters
        ----------
            mode : str
                scattered bosons
            quark_coupling_type : str
                (axial-)vectorial/(axial-)vectorial coupling

        Returns
        -------
            leptonic_coupling : float
                leptonic coupling
        """
        # for CC the polarisation are NOT part of the structure functions, but are accounted for on
        # the cross section level. In order to have a true-trivial LO coeficient function, return
        # here 2.
        if mode == "WW":
            return 2

        # now NC only ...
        projectile_pid = self.obs_config["projectilePID"]
        # correct projectile polarization
        pol = self.obs_config["polarization"]
        if (projectile_pid % 2 == 1 and projectile_pid > 0) or (
            projectile_pid % 2 == 0 and projectile_pid < 0
        ):
            pol *= -1
        # load Z coupling
        projectile_v = 0.0
        projectile_a = 0.0
        if mode in ["phZ", "ZZ"]:
            projectile_v = self.vectorial_coupling(abs(projectile_pid))
            projectile_a = self.weak_isospin_3[abs(projectile_pid)]
        # switch mode
        if mode == "phph":
            if quark_coupling_type in ["VV", "AA"]:
                return self.electric_charge[abs(projectile_pid)] ** 2
            else:
                return 0
        elif mode == "phZ":
            if quark_coupling_type in ["VV", "AA"]:
                return self.electric_charge[abs(projectile_pid)] * (
                    projectile_v + pol * projectile_a
                )
            else:
                return self.electric_charge[abs(projectile_pid)] * (
                    projectile_a + pol * projectile_v
                )
        elif mode == "ZZ":
            if quark_coupling_type in ["VV", "AA"]:
                return (
                    projectile_v ** 2
                    + projectile_a ** 2
                    + 2.0 * pol * projectile_v * projectile_a
                )
            else:
                return 2.0 * projectile_v * projectile_a + pol * (
                    projectile_v ** 2 + projectile_a ** 2
                )
        raise ValueError(f"Unknown mode: {mode}")

    def partonic_coupling(self, mode, pid, quark_coupling_type, cc_mask=None):
        """
        Computes the coupling of the boson to the parton

        Parameters
        ----------
            mode : str
                scattered bosons
            pid : int
                parton identifier
            quark_coupling_type : str
                flag to distinguish for heavy quarks between vectorial and axial-vectorial
                coupling
            cc_mask : str
                observable flavor to determine the heavy flavour couplings in F3

        Returns
        -------
            partonic_coupling : float
                partonic coupling
        """
        # for quarks only the flavor does matter
        pid = abs(pid)
        if mode == "WW":
            return np.sum(self.theory_config["CKM"].masked(cc_mask)(pid))
        # load couplings
        qph = {
            "V": self.electric_charge[pid],
            "A": 0,  # axial coupling of the photon to the quark is not there of course
        }
        qZ = {"V": self.vectorial_coupling(pid), "A": self.weak_isospin_3[pid]}
        first = quark_coupling_type[0]
        second = quark_coupling_type[1]
        # switch mode
        if mode == "phph":
            return qph[first] * qph[second]
        elif mode == "phZ":
            return qph[first] * qZ[second]
        elif mode == "ZZ":
            return qZ[first] * qZ[second]
        raise ValueError(f"Unknown mode: {mode}")

    def propagator_factor(self, mode, Q2):
        """
        Propagator correction to account for different bosons (:math:`\\eta` in PDG)

        Parameters
        ----------
            mode : str
                scattered bosons
            Q2 : float
                virtuality of the process

        Returns
        -------
            propagator_factor : float
                propagator shift
        """
        if mode == "phph":
            return 1
        eta_phZ = (Q2 / (self.theory_config["MZ2"] + Q2)) / (
            4.0
            * self.theory_config["sin2theta_weak"]
            * (1.0 - self.theory_config["sin2theta_weak"])
        )
        eta_phZ /= 1 - self.obs_config["propagatorCorrection"]
        if mode == "phZ":
            return eta_phZ
        if mode == "ZZ":
            return eta_phZ ** 2
        if mode == "WW":
            eta_W = (
                (eta_phZ / 2)
                * (1 + Q2 / self.theory_config["MZ2"])
                / (1 + Q2 / self.theory_config["MW2"])
            ) ** 2
            return eta_W
        raise ValueError(f"Unknown mode: {mode}")

    def get_weight(self, pid, Q2, quark_coupling_type, cc_mask=None):
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
            cc_mask : str
                observable flavor to determine the heavy flavour couplings in F3

        Returns
        -------
            w : float
                weight
        """
        # CC = WW
        if self.obs_config["process"] == "CC":
            return self.leptonic_coupling(
                "WW", quark_coupling_type
            ) * self.partonic_coupling("WW", pid, quark_coupling_type, cc_mask=cc_mask)
        w_phph = (
            self.leptonic_coupling("phph", quark_coupling_type)
            * self.propagator_factor("phph", Q2)
            * self.partonic_coupling("phph", pid, quark_coupling_type)
        )
        # pure photon exchane
        if self.obs_config["process"] == "EM":
            return w_phph
        # allow Z to be mixed in
        if self.obs_config["process"] == "NC":
            # photon-Z interference
            w_phZ = (
                2
                * self.leptonic_coupling("phZ", quark_coupling_type)
                * self.propagator_factor("phZ", Q2)
                * self.partonic_coupling("phZ", pid, quark_coupling_type)
            )
            # true Z contributions
            w_ZZ = (
                self.leptonic_coupling("ZZ", quark_coupling_type)
                * self.propagator_factor("ZZ", Q2)
                * self.partonic_coupling("ZZ", pid, quark_coupling_type)
            )
            return w_phph + w_phZ + w_ZZ
        raise ValueError(f"Unknown process: {self.obs_config['process']}")

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
            "MZ2": theory.get("MZ", 91.1876)
            ** 2,  # TODO remove defaults to the PDG2020 value
            "CKM": CKM2Matrix.from_str(
                theory["CKM"]
            ),  # TODO remove default in PDG2020 Eq. 12.33
            "sin2theta_weak": theory.get(
                "SIN2TW", 0.23121
            ),  # TODO remove defaults to the PDG2020 value
        }
        # set MW
        MW = theory.get("MW")
        if MW is None:
            theory_config["MW2"] = theory_config["MZ2"] / (
                1 - theory_config["sin2theta_weak"]
            )
            # TODO raise warning in log if inconsitent
        else:
            theory_config["MW2"] = MW ** 2

        # map projectile to PID
        proj = observables.get("ProjectileDIS", "electron")
        projectile_pids = {
            "electron": 11,
            "positron": -11,
            "neutrino": 12,
            "antineutrino": -12,
        }
        if proj not in projectile_pids:
            raise ValueError(f"Unknown projectile {proj}")
        obs_config = {
            "process": observables["prDIS"],
            "projectilePID": projectile_pids[proj],
            "polarization": observables["PolarizationDIS"],
            "propagatorCorrection": observables["PropagatorCorrection"],
        }
        o = cls(theory_config, obs_config)
        return o


class CKM2Matrix:
    """
    Wrapper for the CKM matrix

    Parameters
    ----------
        elems : list(float)
            squared elements in row order
    """

    flav_rows = ["u", "c", "t"]
    pid_rows = [2, 4, 6]
    flav_cols = ["d", "s", "b"]
    pid_cols = [1, 3, 5]

    def __init__(self, elems):
        self.m = np.array(elems).reshape(3, 3)
        # TODO maybe raise warning if non-unitarian

    def __repr__(self):
        return "CKM(" + str(self.m).replace("\n", "") + ")"

    def __getitem__(self, key):
        """
        Allows pid and strings as key

        Parameters
        ----------
            key :
                input key

        Returns
        -------
            item :
                element(s)
        """
        nkey = []
        if not isinstance(key, tuple):
            key = (key,)
        if len(key) > 2:
            raise KeyError("CKM matrices are 3x3 matrices")
        for k, flavs, pids in zip(
            key, [self.flav_rows, self.flav_cols], [self.pid_rows, self.pid_cols]
        ):
            if isinstance(k, str):
                nkey.append(flavs.index(k))
            elif isinstance(k, int):
                nkey.append(pids.index(k))
            else:
                nkey.append(k)
        return self.m[tuple(nkey)]

    def __call__(self, pid):
        """
        Get column and row depending on pid

        Parameters
        ----------
            pid : int
                particle identifier

        Returns
        -------
            elems : list(float)
                row or column
        """
        if pid % 2 == 0:
            return self[pid]
        return self[:, pid]

    def masked(self, flavors):
        """
        Apply a mask according to the flavor

        Parameters
        ----------
            flavors : str
                participating flavors as single characters

        Returns
        -------
            matrix : CKMMatrix
                masked matrix
        """
        op = np.zeros((3, 3))
        if "dus" in flavors:
            op += np.array([[1, 1, 0], [0, 0, 0], [0, 0, 0]])
        if "c" in flavors:
            op += np.array([[0, 0, 0], [1, 1, 0], [0, 0, 0]])
        if "b" in flavors:
            op += np.array([[0, 0, 1], [0, 0, 1], [0, 0, 0]])
        if "t" in flavors:
            op += np.array([[0, 0, 0], [0, 0, 0], [1, 1, 1]])
        return type(self)(self.m * op)

    @classmethod
    def from_str(cls, theory_string):
        """
        Create the object from a string representation

        Parameters
        ----------
            theory_string : str
                all elements rowwise in a string


        Returns
        -------
            m : CKMMatrix
                created object
        """
        elems = theory_string.split(" ")
        return cls(np.power(np.array(elems, dtype=float), 2))
