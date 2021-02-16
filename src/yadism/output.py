# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import yaml

from .esf.esf_result import ESFResult
from . import observable_name as on


class Output(dict):
    """
    Wrapper for the output to help with application
    to PDFs and dumping to file.
    """

    def apply_pdf(self, lhapdf_like, alpha_s, xiR, xiF):
        r"""
        Compute all observables for the given PDF.

        Parameters
        ----------
            lhapdf_like : object
                object that provides an xfxQ2 callable (as `lhapdf <https://lhapdf.hepforge.org/>`_
                and :class:`ekomark.toyLH.toyPDF` do) (and thus is in flavor basis)

        Returns
        -------
            res : PDFOutput
                output dictionary with all structure functions for all x, Q2, result and error
        """
        # iterate
        ret = PDFOutput()
        for obs in self:
            if not on.ObservableName.is_valid(obs):
                continue
            if self[obs] is None:
                continue
            ret[obs] = []
            for kin in self[obs]:
                ret[obs].append(
                    kin.apply_pdf(
                        lhapdf_like,
                        self["pids"],
                        self["interpolation_xgrid"],
                        alpha_s,
                        xiR,
                        xiF,
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
        for f in ["interpolation_polynomial_degree", "interpolation_is_log"]:
            out[f] = self[f]
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
        if len(self[obsname]) <= 0:
            raise ValueError(f"no ESF {obsname}!")
        import pineappl #pylint: disable=import-outside-toplevel
        interpolation_xgrid = self["interpolation_xgrid"]
        # interpolation_is_log = self["interpolation_is_log"]
        interpolation_polynomial_degree = self["interpolation_polynomial_degree"]
        lepton_pid = self["projectilePID"]

        # init pineappl objects
        lumi_entries = [pineappl.lumi.LumiEntry([(pid, lepton_pid, 1.0)]) for pid in self["pids"]]
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

        extra = pineappl.subgrid.ExtraSubgridParams()
        extra.set_reweight2(False)
        extra.set_x2_bins(1)
        extra.set_x2_max(1.0)
        extra.set_x2_min(1.0)
        extra.set_x2_order(0)

        grid = pineappl.grid.Grid(
            lumi_entries, orders, bin_limits, pineappl.subgrid.SubgridParams()
        )
        limits = []

        #import pdb; pdb.set_trace()
        # add each ESF as a bin
        for bin_, obs in enumerate(self[obsname]):
            Q2 = obs.Q2
            x = obs.x

            limits.append((Q2, Q2))
            limits.append((x, x))

            params.set_q2_bins(1)
            params.set_q2_max(Q2)
            params.set_q2_min(Q2)
            params.set_q2_order(0)

            for o, (v,_e) in obs.orders.items():
                order_index = list(first_esf_result.orders.keys()).index(o)

                for pid_index, pid_values in enumerate(v):
                    pid_values = list(reversed(pid_values))

                    assert len(pid_values) == params.x_bins()

                    if any(np.array(pid_values) != 0):
                        subgrid = pineappl.lagrange_subgrid.LagrangeSubgridV2(params, extra)
                        subgrid.write_q2_slice(0, pid_values)
                        grid.set_subgrid(order_index, bin_, pid_index, subgrid)
        # set the correct observables
        normalizations = [1.0] * bins
        remapper = pineappl.bin.BinRemapper(normalizations, limits)
        grid.set_remapper(remapper)

        # set the initial state PDF ids for the grid
        grid.set_key_value("initial_state_1", "2212")
        grid.set_key_value("initial_state_2", str(lepton_pid))

        # TODO: find a way to open file in python
        # with open(output_pineappl, "wb") as f:
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
        return cls(obj)

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
        Write all tables to file

        Parameters
        ----------
            filename : str
                output file name
        """
        with open(filename, "w") as f:
            for name, table in self.tables.items():
                f.write("\n".join([name, str(table), "\n"]))
