# -*- coding: utf-8 -*-
from bowler import Query

q = (
    Query("src/yadism/structure_functions")
    .select_module("convolution")
    .rename("distribution_vec")
)
