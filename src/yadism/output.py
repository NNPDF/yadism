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
                        xiF
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
        for f in ["interpolation_polynomial_degree", "interpolation_is_log", "xiF"]:
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
                obj[obs][j] = ESFResult.from_dict(kin)
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
