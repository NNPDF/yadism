# -*- coding: utf-8 -*-

from rope.base.project import Project
from rope.refactor.rename import Rename
from rope.refactor.extract import ExtractVariable
from rope.refactor import restructure

proj = Project('src/yadism/')

#var = proj.get_resource("StructureFunction.py:StructureFunction._interpolator")

sf = proj.get_file('StructureFunction.py')

var = ExtractVariable(proj,sf,36,37)
print(var)
changes = Rename(proj,var.resource).get_changes("self.interpolator")
desc = changes.get_description()

#pattern = '${pow_func}(${param1}, ${param2})'
#goal = '${param1} ** ${param2}'
#args = {'pow_func': 'name=mod1.pow'}
#restructuring = restructure.Restructure(project, pattern, goal, args)
#print(restructure.get_changes().get_description())
print(desc)
#proj.do(changes)