# -*- coding: utf-8 -*-
import copy
import json
import pathlib

import numpy as np
import pandas as pd
import yaml
from eko import strong_coupling

from . import observable_name as on
from .esf.result import ESFResult
from .input import compatibility
from .version import __version__


class MaskedPDF:
    """
    Mask some pids of a PDF set to be 0.

    Parameters
    ----------
        lhapdf_like : callable
            object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
            and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)
        active_pids : list(int)
            active PIDs
    """

    def __init__(self, lhapdf_like, active_pids):
        self.parent = lhapdf_like
        self.active_pids = active_pids

    def __getattr__(self, name):
        return self.parent.__getattribute__(name)

    def xfxQ2(self, pid, x, Q2):
        return self.parent.xfxQ2(pid, x, Q2) if pid in self.active_pids else 0.0


class Output(dict):
    """
    Wrapper for the output to help with application
    to PDFs and dumping to file.
    """

    theory = None
    observables = None

    def apply_pdf(self, lhapdf_like):
        r"""
        Compute all observables for the given PDF.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
                and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)

        Returns
        -------
            ret : PDFOutput
                output dictionary with all structure functions for all x, Q2, result and error
        """
        return self.apply_pdf_theory(lhapdf_like, self.theory)

    def apply_pdf_theory(self, lhapdf_like, theory):
        r"""
        Compute all observables for the given PDF.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
                and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)
            theory : dict
                theory dictionary

        Returns
        -------
            ret : PDFOutput
                output dictionary with all structure functions for all x, Q2, result and error
        """
        new_theory, _ = compatibility.update(theory, dict(TargetDIS="proton"))
        sc = strong_coupling.StrongCoupling.from_dict(new_theory)
        alpha_s = lambda muR: sc.a_s(muR**2) * 4.0 * np.pi
        alpha_qed = lambda _muR: theory["alphaqed"]
        return self.apply_pdf_alphas_alphaqed_xir_xif(
            lhapdf_like, alpha_s, alpha_qed, theory["XIR"], theory["XIF"]
        )

    def apply_pdf_alphas_alphaqed_xir_xif(
        self, lhapdf_like, alpha_s, alpha_qed, xiR, xiF
    ):
        r"""
        Compute all observables for the given PDF.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
                and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)
            alpha_s : callable
                alpha_s(muR)
            alpha_qed : callable
                alpha_qed
            xiR : float
                ratio renormalization scale to virtuality (linear!)
            xiF : float
                ratio factorization scale to virtuality (linear!)

        Returns
        -------
            ret : PDFOutput
                output dictionary with all structure functions for all x, Q2, result and error
        """
        # iterate
        ret = PDFOutput()

        xgrid = self["interpolation_xgrid"]

        # dispatch onto result
        for obs in self:
            if not on.ObservableName.is_valid(obs):
                continue
            if self[obs] is None:
                continue
            ret[obs] = []
            for kin in self[obs]:
                ret[obs].append(
                    kin.apply_pdf(
                        lhapdf_like, self["pids"], xgrid, alpha_s, alpha_qed, xiR, xiF
                    )
                )
        return ret

    def get_raw(self):
        """
        Serialize result as dict.

        This maps the original numpy matrices to lists.

        Returns
        -------
            out : dict
                dictionary which will be written on output
        """
        out = {}
        # dump raw elements
        for f in self:
            out[f] = copy.copy(self[f])
        out["pids"] = list(self["pids"])
        # make raw lists
        for k in ["interpolation_xgrid"]:
            out[k] = self[k].tolist()
        for obs in self:
            if not on.ObservableName.is_valid(obs):
                continue
            if self[obs] is None:
                continue
            out[obs] = []
            for kin in self[obs]:
                out[obs].append(kin.get_raw())
        return out

    def dump_pineappl_to_file(self, filename, obsname):
        """
        Write a pineappl grid to file.

        Parameters
        ----------
            filename : str
                output file name
            obsname : str
                observable to be dumped
        """
        # pylint: disable=no-member, too-many-locals
        if len(self[obsname]) <= 0:
            raise ValueError(f"no ESF {obsname}!")
        import pineappl  # pylint: disable=import-outside-toplevel,import-error

        interpolation_xgrid = self["interpolation_xgrid"]
        # interpolation_is_log = self["interpolation_is_log"]
        interpolation_polynomial_degree = self["interpolation_polynomial_degree"]
        lepton_pid = self["projectilePID"]

        # init pineappl objects
        lumi_entries = [
            pineappl.lumi.LumiEntry([(pid, lepton_pid, 1.0)]) for pid in self["pids"]
        ]
        first_esf_result = self[obsname][0]
        orders = [pineappl.grid.Order(*o) for o in first_esf_result.orders]
        bins = len(self[obsname])
        bin_limits = list(map(float, range(0, bins + 1)))
        # subgrid params
        params = pineappl.subgrid.SubgridParams()
        params.set_reweight(False)
        params.set_x_bins(len(interpolation_xgrid))
        params.set_x_max(interpolation_xgrid[-1])
        params.set_x_min(interpolation_xgrid[0])
        params.set_x_order(interpolation_polynomial_degree)

        grid = pineappl.grid.Grid.create(lumi_entries, orders, bin_limits, params)
        limits = []

        # add each ESF as a bin
        for bin_, obs in enumerate(self[obsname]):
            x = obs.x
            Q2 = obs.Q2

            limits.append((Q2, Q2))
            limits.append((x, x))

            # add all orders
            for o, (v, _e) in obs.orders.items():
                order_index = list(first_esf_result.orders.keys()).index(o)
                prefactor = (
                    ((1.0 / (4.0 * np.pi)) ** o[0])
                    * ((-1.0) ** o[2])
                    * ((-1.0) ** o[3])
                )
                # add for each pid/lumi
                for pid_index, pid_values in enumerate(v):
                    pid_values = prefactor * pid_values
                    # grid is empty? skip
                    if not any(np.array(pid_values) != 0):
                        continue
                    subgrid = pineappl.import_only_subgrid.ImportOnlySubgridV1(
                        pid_values[np.newaxis, :, np.newaxis],
                        [Q2],
                        interpolation_xgrid,
                        [1.0],
                    )
                    grid.set_subgrid(order_index, bin_, pid_index, subgrid)
        # set the correct observables
        normalizations = [1.0] * bins
        remapper = pineappl.bin.BinRemapper(normalizations, limits)
        grid.set_remapper(remapper)

        # set the initial state PDF ids for the grid
        grid.set_key_value("initial_state_1", "2212")
        grid.set_key_value("initial_state_2", str(lepton_pid))
        grid.set_key_value("theory", json.dumps(self.theory))
        grid.set_key_value("runcard", json.dumps(self.observables))
        grid.set_key_value("yadism_version", __version__)
        grid.set_key_value("lumi_id_types", "pdg_mc_ids")

        # dump file
        grid.optimize()
        grid.write(filename)

    def dump_yaml(self, stream=None):
        """
        Serialize result as YAML.

        Parameters
        ----------
            stream : None or stream
                if given, dump is written on it

        Returns
        -------
            dump : any
                result of dump(output, stream), i.e. a string, if no stream is given or
                Null, if self is written sucessfully to stream
        """
        # TODO explicitly silence yaml
        out = self.get_raw()
        out["theory"] = self.theory
        out["observables"] = self.observables
        return yaml.dump(out, stream)

    def dump_yaml_to_file(self, filename):
        """
        Writes YAML representation to a file.

        Parameters
        ----------
            filename : string
                target file name

        Returns
        -------
            ret : any
                result of dump(output, stream), i.e. Null if written sucessfully
        """
        with open(filename, "w") as f:
            ret = self.dump_yaml(f)
        return ret

    @classmethod
    def load_yaml(cls, stream):
        """
        Load YAML representation from stream

        Parameters
        ----------
            stream : any
                source stream

        Returns
        -------
            obj : cls
                loaded object
        """
        obj = yaml.safe_load(stream)
        # make list numpy
        for k in ["interpolation_xgrid"]:
            obj[k] = np.array(obj[k])
        for obs in obj:
            if not on.ObservableName.is_valid(obs):
                continue
            if obj[obs] is None:
                continue
            for j, kin in enumerate(obj[obs]):
                obj[obs][j] = ESFResult.from_document(kin)

        out = cls(obj)
        out.theory = obj["theory"]
        out.observables = obj["observables"]
        del out["theory"]
        del out["observables"]
        return out

    @classmethod
    def load_yaml_from_file(cls, filename):
        """
        Load YAML representation from file

        Parameters
        ----------
            filename : string
                source file name

        Returns
        -------
            obj : cls
                loaded object
        """
        obj = None
        with open(filename) as o:
            obj = cls.load_yaml(o)
        return obj


class PDFOutput(Output):
    """
    Wrapper for the PDF output to help with dumping to file.
    """

    def get_raw(self):
        """
        Convert the object into a native Python dictionary

        Returns
        -------
            out : dict
                raw dictionary
        """
        out = {}
        for obs in self:
            if self[obs] is None:
                continue
            out[obs] = []
            for kin in self[obs]:
                out[obs].append({k: float(v) for k, v in kin.items()})
        return out

    @classmethod
    def load_yaml(cls, stream):
        """
        Load the object from YAML.

        Parameters
        ----------
            stream : any
                source stream

        Returns
        -------
            obj : cls
                created object
        """
        obj = yaml.safe_load(stream)
        return cls(obj)

    @property
    def tables(self):
        """
        Convert data into a mapping structure functions -> pandas DataFrame
        """
        tables = {}
        for k, v in self.items():
            tables[k] = pd.DataFrame(v)

        return tables

    def dump_tables_to_file(self, filename):
        """
        Write all tables to file.

        Parameters
        ----------
            filename : str
                output file name
        """
        with open(filename, "w") as f:
            for name, table in self.tables.items():
                f.write("\n".join([name, str(table), "\n"]))

    def dump_tables_to_csv(self, dirname):
        """
        Write all tables to separate csv files.

        Parameters
        ----------
            dirname : str
                output directory name
        """
        dirname = pathlib.Path(dirname)
        dirname.mkdir(exist_ok=True)
        for name, table in self.tables.items():
            filename = dirname / f"{name}.csv"
            table.to_csv(filename)
