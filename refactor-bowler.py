# -*- coding: utf-8 -*-
from bowler import Query

q = (
    Query("src/yadism")
    .select_class("Runner")
    .select_attribute("_observable_instances")
    .rename("observable_instances")
)
