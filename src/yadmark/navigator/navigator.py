from banana import navigator as bnav

from yadism import observable_name as on

from ..data import db

table_objects = bnav.navigator.table_objects
table_objects["o"] = db.Observable


class NavigatorApp(bnav.navigator.NavigatorApp):
    """
    Navigator base class holding all elementry operations.

    Parameters
    ----------
        cfg : dict
            banana configuration
        mode : string
            mode identifier
    """

    myname = "yadism"
    table_objects = table_objects

    def fill_theories(self, theo, obj):
        """
        Collect important information of the theory record.

        Parameters
        ----------
            theo : dict
                database record
            obj : dict
                to be updated pandas record
        """
        for f in ["PTO", "XIF", "XIR", "TMC", "NfFF", "FNS", "DAMP", "IC"]:
            obj[f] = theo[f]

    def fill_observables(self, ob, obj):
        """
        Collect important information of the observable record.

        Parameters
        ----------
            theo : dict
                database record
            obj : dict
                to be updated pandas record
        """
        if "PTO" in ob:
            obj["PTO"] = ob["PTO"]
        xgrid = ob["interpolation_xgrid"]
        obj["xgrid"] = (
            f"{len(xgrid)}pts: "
            + f"{'log' if ob['interpolation_is_log'] else 'x'}"
            + f"^{ob['interpolation_polynomial_degree']}"
        )
        obj["curr"] = ob["prDIS"]
        proj_map = {
            "electron": "e-",
            "positron": "e+",
            "neutrino": "ν",
            "antineutrino": "ν~",
        }
        obj["proj"] = proj_map[ob["ProjectileDIS"]]
        obj["pol"] = ob["PolarizationDIS"]
        sfs = 0
        esfs = 0
        for esfs_dict in ob["observables"].values():
            sfs += 1
            esfs += len(esfs_dict)
        obj["structure_functions"] = f"{sfs} SF @ {esfs} points"

    def fill_cache(self, cac, obj):
        """
        Collect important information of the cache record.

        Parameters
        ----------
            cac : dict
                database record
            obj : dict
                to be updated pandas record
        """
        sfs = 0
        esfs = 0
        for esfs_dict in cac["result"].values():
            sfs += 1
            esfs += len(esfs_dict)
        obj["structure_functions"] = f"{sfs} SF @ {esfs} pts"

        obj["theory"] = cac["t_hash"][: self.hash_len]
        obj["ocard"] = cac["o_hash"][: self.hash_len]
        for f in ["pdf", "external"]:
            obj[f] = cac[f]

    def fill_logs(self, lg, obj):
        """
        Collect important information of the log record.

        Parameters
        ----------
        lg : dict
            database record
        obj : dict
            to be updated pandas record
        """
        sfs = 0
        esfs = 0
        for esfs_dict in lg["log"].values():
            sfs += 1
            esfs += len(esfs_dict)
        crash = lg.get("_crash", None)
        if crash is None:
            obj["structure_functions"] = f"{sfs} SF @ {esfs} pts"
        else:
            obj["structure_functions"] = crash

        obj["theory"] = lg["t_hash"][: self.hash_len]
        obj["ocard"] = lg["o_hash"][: self.hash_len]
        obj["pdf"] = lg["pdf"]
        obj["external"] = lg["external"]

    def check_log(self, doc_hash, perc_thr=1, abs_thr=1e-6):
        """
        Check if the log passed the default assertions

        Parameters
        ---------
            doc_hash : hash
                log hash
        """
        # TODO determine external, improve output
        dfd = self.log_as_dfd(doc_hash)
        for n, df in dfd.items():
            for l in df.iloc:
                if (
                    abs(l["percent_error"]) > perc_thr
                    and abs(l["APFEL"] - l["yadism"]) > abs_thr
                ):
                    print(n, l, sep="\n", end="\n\n")

    @staticmethod
    def is_valid_physical_object(name):
        return on.ObservableName.is_valid(name)

    # def join(self, id1, id2):
    #     tabs = []
    #     tabs1 = []
    #     exts = []
    #     suffixes = (f" ({id1})", f" ({id2})")

    #     for i, doc_hash in enumerate([id1, id2]):
    #         tabs += [self.get_log_DFdict(doc_hash)[0]]
    #         tabs1 += [tabs[i].drop(["yadism", "yadism_error", "percent_error"], axis=1)]
    #         exts += [
    #             tabs1[i].columns.drop(["x", "Q2"])[0]
    #         ]  # + suffixes[i]] # to do: the suffixes are not working as expected

    #     def rel_err(row):
    #         ref = row[exts[0]]
    #         cmp = row[exts[1]]
    #         if ref != 0:
    #             return (cmp / ref - 1) * 100
    #         else:
    #             return np.nan

    #     tab_joint = tabs1[0].merge(
    #         tabs1[1], on=["x", "Q2"], how="outer", suffixes=suffixes
    #     )
    #     tab_joint["ext_rel_err [%]"] = tab_joint.apply(rel_err, axis=1)

    #     if all(np.isclose(tabs[0]["yadism"], tabs[1]["yadism"])):
    #         tab_joint["yadism"] = tabs[0]["yadism"]
    #         tab_joint["yadism_error"] = tabs[0]["yadism_error"]
    #     else:
    #         pass

    #     return tab_joint
