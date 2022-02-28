# -*- coding: utf-8 -*-
import io
from unittest import mock
import tarfile
import numpy as np
import pytest
import pathlib
from yadism import output
from yadism.esf import result

lo = (0, 0, 0, 0)


class MockPDFgonly:
    def hasFlavor(self, pid):
        return pid == 21

    def xfxQ2(self, pid, x, Q2):
        if pid == 21:
            return x**2 * Q2  # it is xfxQ2! beware of the additional x
        return 0


class TestOutput:
    def fake_output(self):
        out = dict()
        out["interpolation_xgrid"] = np.array([0.5, 1.0])
        out["interpolation_polynomial_degree"] = 1
        out["interpolation_is_log"] = True
        out["pids"] = [21, 1]
        out["_ciao"] = "come va?"

        obs = ["F2_total", "FL_total", "F3_total"]

        for o in obs:
            o_esf = []
            # test Q2 values
            for Q2 in [1, 10, 100]:
                kin = dict(
                    x=0.5,
                    Q2=Q2,
                    orders={
                        lo: (np.array([[1, 0], [0, 1]]), np.array([[1, 0], [0, 1]]))
                    },
                )
                # plain
                o_esf.append(result.ESFResult(**kin, nf=3))

            out[o] = o_esf

        out["F2_light"] = None
        return out, obs

    def test_apply_pdf(self):
        out, obs = self.fake_output()
        outp = output.Output()
        outp.update(out)

        ret = outp.apply_pdf_alphas_alphaqed_xir_xif(
            MockPDFgonly(), lambda _muR: 1, lambda _muR: 1, 1.0, 1.0
        )
        for o in obs:
            for a, pra in zip(out[o], ret[o]):
                expexted_res = a.orders[lo][0][0][0] * a.x * a.Q2
                expected_err = np.abs(a.orders[lo][0][0][0]) * a.x * a.Q2
                assert pytest.approx(pra["result"], 0, 0) == expexted_res
                assert pytest.approx(pra["error"], 0, 0) == expected_err

        # test factorization scale variation
        for xiF in [0.5, 2.0]:

            ret = outp.apply_pdf_alphas_alphaqed_xir_xif(
                MockPDFgonly(), lambda _muR: 1, lambda _muR: 1, 1.0, xiF
            )
            for a, pra in zip(out["F2_total"], ret["F2_total"]):
                expexted_res = a.orders[lo][0][0][0] * a.x * a.Q2
                expected_err = np.abs(a.orders[lo][0][0][0]) * a.x * a.Q2
                assert pytest.approx(pra["result"], 0, 0) == expexted_res * xiF**2
                assert pytest.approx(pra["error"], 0, 0) == expected_err * xiF**2

    def test_io(self):
        d, _obs = self.fake_output()
        # create object
        o1 = output.Output(d)
        # test streams
        stream = io.StringIO()
        o1.dump_yaml(stream)
        # rewind and read again
        stream.seek(0)
        o2 = output.Output.load_yaml(stream)
        np.testing.assert_almost_equal(
            o1["interpolation_xgrid"], d["interpolation_xgrid"]
        )
        np.testing.assert_almost_equal(
            o2["interpolation_xgrid"], d["interpolation_xgrid"]
        )
        # fake output files
        m_out = mock.mock_open(read_data="")
        with mock.patch("builtins.open", m_out) as mock_file:
            fn = "test.yaml"
            o1.dump_yaml_to_file(fn)
            mock_file.assert_called_with(fn, "w")
        # fake input file
        stream.seek(0)
        m_in = mock.mock_open(read_data=stream.getvalue())
        with mock.patch("builtins.open", m_in) as mock_file:
            fn = "test.yaml"
            o3 = output.Output.load_yaml_from_file(fn)
            mock_file.assert_called_with(fn)
            np.testing.assert_almost_equal(
                o3["interpolation_xgrid"], d["interpolation_xgrid"]
            )
    
    def test_tar_output(self, tmp_path):
        out, obs = self.fake_output()
        #dump fake output
        o1 = output.Output(out)
        temp_path = pathlib.Path(tmp_path)
        fn = pathlib.Path("test.tar")
        actual_path = pathlib.PurePath(temp_path, fn)
        o1.dump_tar(actual_path)
        #load fake output
        r1 = output.Output.load_tar(actual_path)
        #test they are equal
        np.testing.assert_almost_equal(
                o1["interpolation_xgrid"], r1["interpolation_xgrid"]
            )
        np.testing.assert_almost_equal(
                o1["pids"], r1["pids"]
            )
        np.testing.assert_equal(len(o1), len(r1))
        np.testing.assert_equal(type(o1), type(r1))

            



        

   
