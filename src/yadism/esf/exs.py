from ..observable_name import ObservableName

class EvaluatedCrossSection:
    def __init__(self, xs, kin):
        self.xs = xs
        self.kin = kin

    def get_result(self):
        f2 = self.xs.get_esf(ObservableName("F2light"),self.kin).get_result()
        fl = self.xs.get_esf(ObservableName("FLlight"),self.kin).get_result()
        f3 = self.xs.get_esf(ObservableName("F3light"),self.kin).get_result()
        #import pdb; pdb.set_trace()
        return f2 + fl + f3
