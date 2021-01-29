# -*- coding: utf-8 -*-
from datetime import datetime

import tinydb


def get_external_data(theory, observables, pdf, cache_table, cb_compute_data):
    """
    Run external source to compute observables or simply use cached values.

    Parameters
    ----------
        theory : dict
            theory runcard
        observables : dict
            observables runcard
        pdf : Any
            PDF object (LHAPDF like)
        cache_table : tinyDB.Table
            caching table
        cb_compute_data : callable
            callback to compute the actual data (if caching isn't succesfull)

    Returns
    -------
        tab : dict
            external numbers
    """
    pdf_name = pdf.set().name
    # search for document in the cache
    cache_query = tinydb.Query()
    c_query = (
        cache_query._theory_doc_id == theory.doc_id  # pylint:disable=protected-access
    )  # pylint:disable=protected-access
    c_query &= (
        cache_query._observables_doc_id == observables.doc_id
    )  # pylint:disable=protected-access
    c_query &= cache_query._pdf == pdf_name  # pylint:disable=protected-access
    query_res = cache_table.search(c_query)

    tab = None
    # check if cache existing
    if len(query_res) == 1:
        tab = query_res[0]
    elif len(query_res) > 1:
        raise ValueError("Cache query matched more than once.")
    # check is updated
    if tab is not None:
        theory_changed = datetime.fromisoformat(theory["_created"])
        obs_changed = datetime.fromisoformat(observables["_created"])
        tab_changed = datetime.fromisoformat(tab["_creation_time"])
        if (theory_changed - tab_changed).total_seconds() > 0 or (
            obs_changed - tab_changed
        ).total_seconds() > 0:
            # delete old one
            cache_table.remove(doc_ids=[tab.doc_id])
            tab = None
    # cached or recompute
    if tab is not None:
        return tab
    else:
        tab = cb_compute_data(theory, observables, pdf)

    # store the cache
    tab["_theory_doc_id"] = theory.doc_id
    tab["_observables_doc_id"] = observables.doc_id
    tab["_pdf"] = pdf_name
    tab["_creation_time"] = datetime.now().isoformat()
    cache_table.insert(tab)

    return tab
