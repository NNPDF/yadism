# -*- coding: utf-8 -*-

from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.refactor.extract import ExtractVariable


proj = Project('src/yadism/')

#var = proj.get_resource("StructureFunction.py:StructureFunction._interpolator")

sf = proj.get_file('StructureFunction.py')

#var = ExtractVariable(proj,sf,36,37)
#print(var)
changes = Rename(proj,sf,sf.read().index("_interpolator")+1).get_changes("interpolator")
desc = changes.get_description()
print(desc)

#proj.do(changes)
