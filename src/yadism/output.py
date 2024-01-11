"""
Output related utilities.

For the main output (that is the computed |PDF|
independent |DIS| operator) three outputs are provided:

- tar archive, containing metadata and binary :mod:`numpy.lib.format` arrays
  (this is the **suggested** output format)
- single file `yaml <https://yaml.org/>`_ output: a single human readable (but
  possibly huge) file
- `PineAPPL <https://github.com/N3PDF/pineappl>`_ interpolation grid: very
  useful to store in a standard format (supporting also non-|DIS| processes) and
  interfacing to other codes (but *no loading* is supported from this format)

"""
import copy
import pathlib
import tarfile
import tempfile

import numpy as np
import pandas as pd
import yaml
from eko.couplings import Couplings, couplings_mod_ev
from eko.io import dictlike, runcards, types
from eko.matchings import Atlas, nf_default
from eko.quantities.heavy_quarks import MatchingScales

from . import observable_name as on
from .esf.result import ESFResult, EXSResult


class MaskedPDF:
    """Mask some pids of a PDF set to be 0.

    Parameters
    ----------
    lhapdf_like : callable
        object that provides an xfxQ2 callable (as `lhapdf
        <https://lhapdf.hepforge.org/>`_ and :class:`ekomark.toyLH.toyPDF` do)
        (and thus is in flavor basis)
    active_pids : list[int]
        active PIDs

    """

    def __init__(self, lhapdf_like, active_pids):
        self.parent = lhapdf_like
        self.active_pids = active_pids

    def __getattr__(self, name):
        return self.parent.__getattribute__(name)

    def xfxQ2(self, pid, x, Q2):
        """Fake lhapdf-like wrapper."""
        return self.parent.xfxQ2(pid, x, Q2) if pid in self.active_pids else 0.0


class Output(dict):
    """Wrapper for the output to help with application to PDFs and dumping to file."""

    theory = None
    observables = None

    def apply_pdf(self, lhapdf_like):
        r"""Compute all observables for the given PDF.

        Parameters
        ----------
        lhapdf_like : object
            object that provides an xfxQ2 callable (as `lhapdf
            <https://lhapdf.hepforge.org/>`_ and :class:`ekomark.toyLH.toyPDF`
            do) (and thus is in flavor basis)

        Returns
        -------
        ret : :class:`PDFOutput`
            output dictionary with all structure functions for all x, Q2, result and error

        """
        return self.apply_pdf_theory(lhapdf_like, self.theory)

    def apply_pdf_theory(self, lhapdf_like, theory):
        r"""Compute all observables for the given PDF.

        Parameters
        ----------
        lhapdf_like : object
            object that provides an xfxQ2 callable (as `lhapdf
            <https://lhapdf.hepforge.org/>`_ and :class:`ekomark.toyLH.toyPDF`
            do) (and thus is in flavor basis)
        theory : dict
            theory dictionary

        Returns
        -------
        ret : :class:`PDFOutput`
            output dictionary with all structure functions for all x, Q2, result and error

        """
        new_eko_theory = runcards.Legacy(theory=theory, operator={}).new_theory
        method = runcards.Legacy.MOD_EV2METHOD.get(theory["ModEv"], theory["ModEv"])
        method = dictlike.load_enum(types.EvolutionMethod, method)
        method = couplings_mod_ev(method)
        masses = [mq**2 for mq, _ in new_eko_theory.heavy.masses]
        thresholds_ratios = np.power(new_eko_theory.heavy.matching_ratios, 2)
        sc = Couplings(
            couplings=new_eko_theory.couplings,
            order=new_eko_theory.order,
            method=method,
            masses=masses,
            hqm_scheme=new_eko_theory.heavy.masses_scheme,
            thresholds_ratios=thresholds_ratios.tolist(),
        )
        atlas = Atlas(
            matching_scales=MatchingScales(masses * thresholds_ratios),
            origin=(theory["Qref"] ** 2, theory["nfref"]),
        )
        fns = theory["FNS"]
        if "FFNS" in fns or "FFN0" in fns:
            alpha_s = lambda muR: sc.a_s(muR**2, nf_to=theory["NfFF"]) * 4.0 * np.pi
        elif fns == "ZM-VFNS":
            alpha_s = (
                lambda muR: sc.a_s(muR**2, nf_to=nf_default(muR**2, atlas))
                * 4.0
                * np.pi
            )
        else:
            raise ValueError(f"Scheme '{fns}' not recognized.")
        alpha_qed = lambda _muR: theory["alphaqed"]
        return self.apply_pdf_alphas_alphaqed_xir_xif(
            lhapdf_like, alpha_s, alpha_qed, theory["XIR"], theory["XIF"]
        )

    def apply_pdf_alphas_alphaqed_xir_xif(
        self, lhapdf_like, alpha_s, alpha_qed, xiR, xiF
    ):
        r"""Compute all observables for the given PDF.

        Parameters
        ----------
        lhapdf_like : object
            object that provides an xfxQ2 callable (as `lhapdf
            <https://lhapdf.hepforge.org/>`_ and :class:`ekomark.toyLH.toyPDF`
            do) (and thus is in flavor basis)
        alpha_s : callable
            :math:`\alpha_s(\mu_R)`, the running strong coupling
        alpha_qed : callable
            :math:`\alpha(\mu_R)`, the running fine structure constant
        xiR : float
            ratio renormalization scale to |EW| boson virtuality (linear!)
        xiF : float
            ratio factorization scale to |EW| boson virtuality (linear!)

        Returns
        -------
        ret : :class:`PDFOutput`
            output dictionary with all structure functions for all :math:`x`,
            :math:`Q^2`, result and error

        """
        # iterate
        ret = PDFOutput()

        xgrid = self["xgrid"]["grid"]

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
        """Serialize result as dict.

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
        for k in ["xgrid"]:
            out[k]["grid"] = self[k]["grid"]
            out[k]["log"] = self[k]["log"]
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
        """Serialize result as YAML.

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
        return yaml.dump(out, stream, default_flow_style=None)

    def dump_yaml_to_file(self, filename):
        """Write YAML representation to a file.

        Parameters
        ----------
        filename : str or os.PathLike
            target file name

        Returns
        -------
        ret : any
            result of dump(output, stream), i.e. Null if written sucessfully

        """
        with open(filename, "w", encoding="utf8") as f:
            ret = self.dump_yaml(f)
        return ret

    def dump_tar(self, tarpath, runcards=True):
        """Serialize output in a tar archive.

        This is the favorite *native* output.

        This results in a considerably smaller output file, with respect to the
        'yaml' serialization, but it looses the readability.
        In most cases, there is no advantage in having a readable DIS operator,
        so they are serialized in binary arrays (see :mod:`numpy.lib.format`).

        This **only supports** observables with a uniform order across
        kinematical point (as they are generated by
        :class:`yadism.runner.Runner`), since they are stored in a unique array.
        They don't have to be uniform across different observables (since they
        are stored in different arrays anyhow).

        Parameters
        ----------
        tarpath : str or os.PathLike
            target file path (it has to have the '.tar' extension)

        Raises
        ------
        AssertionError
            If orders are not uniform within a single observable.

        """
        tarpath = pathlib.Path(tarpath)
        if tarpath.suffix != ".tar":
            raise ValueError(f"'{tarpath}' is not a valid tar filename, wrong suffix")

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)

            metadata = {}
            for metafield, metavalue in self.items():
                if not on.ObservableName.is_valid(metafield) or metavalue is None:
                    # this way even scalar types are properly casted
                    # it works for sure for: None, bool, int, float, str
                    # and so everything we need (what is safe in yaml)
                    metadata[metafield] = np.array(metavalue).tolist()
                else:
                    kinematics = {}
                    for key in metavalue[0].get_raw():
                        if key != "orders":
                            kinematics[key] = []

                    orders_first = []
                    values = []
                    errors = []
                    for esfres in metavalue:
                        orders = []
                        esf_values = []
                        esf_errors = []
                        for key, value in esfres.get_raw().items():
                            if key != "orders":
                                kinematics[key].append(value)
                            else:
                                for order in value:
                                    orders.append(order["order"])
                                    esf_values.append(order["values"])
                                    esf_errors.append(order["errors"])

                        if len(orders_first) == 0:
                            orders_first = orders
                        else:
                            assert orders_first == orders
                        values.append(esf_values)
                        errors.append(esf_errors)

                    np.savez_compressed(
                        tmpdir / metafield,
                        values=np.array(values),
                        errors=np.array(errors),
                    )
                    metadata[metafield] = dict(
                        orders=orders_first, kinematics=kinematics
                    )

            (tmpdir / "metadata.yaml").write_text(
                yaml.safe_dump(metadata, default_flow_style=None), encoding="utf-8"
            )
            if runcards:
                runcards = tmpdir / "runcards"
                runcards.mkdir()
                (runcards / "theory.yaml").write_text(
                    yaml.safe_dump(self.theory), encoding="utf-8"
                )
                (runcards / "observables.yaml").write_text(
                    yaml.safe_dump(self.observables, default_flow_style=None),
                    encoding="utf-8",
                )

            with tarfile.open(tarpath, "w") as tar:
                tar.add(tmpdir, arcname=tarpath.stem)

    @classmethod
    def load_tar(cls, tarpath):
        """Deserialize output object from tar.

        It loads an :meth:`Output.dump_tar` generated tar file into an
        :class:`Output` object.

        Parameters
        ----------
        tarpath : str or os.PathLike
            target file path (it has to be a 'tar' archive)

        Returns
        -------
        :class:`Output`
            loaded object

        """
        tarpath = pathlib.Path(tarpath)

        # Initialize output object
        out = cls()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = pathlib.Path(tmpdir)

            with tarfile.open(tarpath, "r") as tar:
                tar.extractall(tmpdir)

            # The internal name is the one that has been used to save, since the
            # tar could have been renamed in the meanwhile, it might be unknown,
            # but there is only a single folder
            innerdir = list(tmpdir.glob("*"))[0]

            runcards = innerdir / "runcards"
            out.theory = yaml.safe_load((runcards / "theory.yaml").read_text())
            out.observables = yaml.safe_load(
                (runcards / "observables.yaml").read_text()
            )

            metadata = yaml.safe_load((innerdir / "metadata.yaml").read_text())
            for metafield, metavalue in metadata.items():
                if not on.ObservableName.is_valid(metafield) or metavalue is None:
                    ar = np.array(metavalue)
                    if ar.ndim > 0:
                        out[metafield] = ar
                    else:
                        out[metafield] = metavalue
                else:
                    op = np.load(innerdir / f"{metafield}.npz")
                    kinvars, kinvalues = list(zip(*metavalue["kinematics"].items()))
                    kinematics = [dict(zip(kinvars, kin)) for kin in zip(*kinvalues)]
                    orders = metavalue["orders"]

                    Result = ESFResult if "y" not in kinvars else EXSResult
                    results = []

                    for kin, val, err in zip(kinematics, op["values"], op["errors"]):
                        res = kin.copy()
                        res["orders"] = [
                            dict(zip(["order", "values", "errors"], ordvalerr))
                            for ordvalerr in zip(orders, val, err)
                        ]
                        results.append(Result.from_document(res))

                    out[metafield] = results

        return out

    @classmethod
    def load_yaml(cls, stream):
        """Load YAML representation from stream.

        Parameters
        ----------
        stream : any
            source stream

        Returns
        -------
        obj : :class:`Output`
            loaded object

        """
        obj = yaml.safe_load(stream)
        # make list numpy
        for k in ["xgrid"]:
            obj[k]["grid"] = np.array(obj[k]["grid"])
            obj[k]["log"] = obj[k]["log"]
        for obs in obj:
            if not on.ObservableName.is_valid(obs):
                continue
            if obj[obs] is None:
                continue
            Result = ESFResult if "y" not in obj[obs][0] else EXSResult
            for j, kin in enumerate(obj[obs]):
                obj[obs][j] = Result.from_document(kin)

        out = cls(obj)
        out.theory = obj["theory"]
        out.observables = obj["observables"]
        del out["theory"]
        del out["observables"]
        return out

    @classmethod
    def load_yaml_from_file(cls, filename):
        """Load YAML representation from file.

        Parameters
        ----------
        filename : str or os.PathLike
            source file name

        Returns
        -------
        obj : :class:`Output`
            loaded object

        """
        obj = None
        with open(filename) as o:
            obj = cls.load_yaml(o)
        return obj


class PDFOutput(Output):
    """Wrapper for the PDF output to help with dumping to file."""

    def get_raw(self):
        """Convert the object into a native Python dictionary.

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
        """Load the object from YAML.

        Parameters
        ----------
        stream : any
            source stream

        Returns
        -------
        obj : :class:`PDFOutput`
            loaded object

        """
        obj = yaml.safe_load(stream)
        return cls(obj)

    @property
    def tables(self):
        """Convert data into a mapping structure functions -> :class:`pandas.DataFrame`."""
        tables = {}
        for k, v in self.items():
            tables[k] = pd.DataFrame(v)

        return tables

    def dump_tables_to_file(self, filename):
        """Write all tables to file.

        Parameters
        ----------
        filename : str
            output file name

        """
        with open(filename, "w") as f:
            for name, table in self.tables.items():
                f.write("\n".join([name, str(table), "\n"]))

    def dump_tables_to_csv(self, dirname):
        """Write all tables to separate csv files.

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
