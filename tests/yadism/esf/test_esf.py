from yadism.esf.esf import ESFInfo


class TestESFInfo:
    def test_init(self):
        obsn = "ciao"
        confs = "come"
        ESFInfo(obsn, confs)

    def test_getattribute(self):
        class MyObj:
            def __init__(self, come=""):
                self.come = come

        obsn = "ciao"
        confs = MyObj()
        confs.come = "va"
        e = ESFInfo(obsn, confs)

        assert e.obs_name == obsn
        assert e.configs == confs
        assert e.come == confs.come
