# -*- coding: utf-8 -*-

import black

import ic

r = ic.MmaRunner()

data = ic.parse(r, ic.prepare(ic.f3hat), "Rminus")

res = [ic.post_process(r) for r in data]
for r in res:
    print("=" * 10)
    print(black.format_str(r, mode=black.FileMode()))
