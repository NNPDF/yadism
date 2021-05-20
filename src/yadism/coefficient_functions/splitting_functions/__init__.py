from . import lo


class SFConv:
    def __init__(self):
        self.coeffs = {}
        self.coeffs[(1, 0)] = self.c10
        self.coeffs[(1, 1)] = self.c11


class LOns(SFConv):
    pass


class NLOns(SFConv):
    def c10(self):
        return lo.pqq


class NNLOns(SFConv):
    def c10(self):
        #  return nlo.pqq
        pass


nonsinglet = [LOns, NLOns, NNLOns]


fact_list = {((1, 1), 0): lo.pqq}


#  def c211
