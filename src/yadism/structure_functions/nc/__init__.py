import abc


class NeutralCurrent:
    @property
    def components(self):
        return {
            "q": (self.quark_0, self.quark_1, self.quark_1_fact),
            "g": (self.gluon_0, self.gluon_1, self.gluon_1_fact),
        }

    @abc.abstractmethod
    def quark_0(self):
        """
            quark coefficient function at order 0 in :math`a_s`
        """

    @abc.abstractmethod
    def quark_1(self):
        """
            quark coefficient function at order 1 in :math`a_s`
        """

    @abc.abstractmethod
    def quark_1_fact(self):
        pass

    def gluon_0(self):
        return 0

    @abc.abstractmethod
    def gluon_1(self):
        pass

    def gluon_1_fact(self):
        return 0
