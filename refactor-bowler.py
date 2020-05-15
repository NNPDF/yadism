# -*- coding: utf-8 -*-
from bowler import Query

var_name = ["pto", "xiR", "xiF", "M2hq", "TMC", "M2target"]

qs = []
for n in var_name:
    qs.append(Query("src/yadism").select_class("StructureFunction").select_attribute("_"+n).rename(n))
