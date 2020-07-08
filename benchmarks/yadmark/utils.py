# -*- coding: utf-8 -*-
from datetime import datetime

def str_datetime(dt):
    return str(dt)


def unstr_datetime(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")
