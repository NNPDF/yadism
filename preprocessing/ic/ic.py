# -*- coding: utf-8 -*-
import re
import subprocess
import threading
import io


def writeall(p, res):
    while True:
        # print("read data: ")
        data = p.stdout.read(1).decode("utf-8")
        if not data or data == "@":
            break
        res.write(data)
        res.flush()


class MmaRunner:
    def __init__(self):
        self.p = subprocess.Popen(
            ["math", "-noprompt"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
        )

    def send(self, code):
        stream = io.StringIO()
        writer = threading.Thread(target=writeall, args=(self.p, stream))
        writer.start()

        self.p.stdin.write((code + 'Print["@"];\n').encode())
        self.p.stdin.flush()
        writer.join()
        stream.seek(0)
        s = stream.read()
        return s[1:-2].strip()

    def close(self):
        self.send("Exit[];")


def prepare(fform):
    fform = re.sub("\n *\\d", "", fform)
    fform = fform.replace("d0", "")
    fform = fform.replace("s1h2", "s1h**2")
    fform = fform.replace("Del2", "Del**2")
    fform = fform.replace("Delp2", "Delp**2")
    fform = fform.replace("**", "^")
    return fform


def parse(runner, fhat, Spm):
    code_fhat = f"""fhat = {fhat};
    fcoeff = Coefficient[fhat, {Spm}];
    fcoeff = fcoeff /. {{Ixi->(s1h+2m22)/(s1h^2) + (s1h+m22)/(Delp*s1h^2)*Spp*Lxi}};
    Print@FortranForm@Collect[fcoeff,{{Lxi}},FullSimplify];"""
    res_fhat = runner.send(code_fhat)
    code_hcoeff = """gcoeff = zeroAt1 * s1h/(8*(s1h + m22)) * fcoeff;
    gcoeff = gcoeff /. {s1h -> zeroAt1 * s1hreg};
    hcoeff = Limit[gcoeff,zeroAt1->0];
    hcoeff = hcoeff /. {Delp -> Del, Lxi -> Lxisoft, s1hreg -> Del};
    Print@FortranForm@Collect[hcoeff,{Lxi},FullSimplify];"""
    res_ghat_at_1 = runner.send(code_hcoeff)
    return [res_fhat, res_ghat_at_1]

def post_process(res):
    # replace all variables
    res = res.replace("m12", "self.m1sq").replace("m22", "self.m2sq")
    res = (
        res.replace("Spp", "self.sigma_pp")
        .replace("Spm", "self.sigma_pm")
        .replace("Smp", "self.sigma_mp")
    )
    res = res.replace("Del", "self.delta").replace("Delp", "self.deltap")
    res = (
        res.replace("Lxi", "self.L_xi")
        .replace("Ixi", "self.I_xi")
        .replace("s1h", "self.s1hat")
    )
    res = res.replace("Q2IC", "self.ESF.Q2")
    res = res.replace("m1*m2", "np.sqrt(self.m1sq * self.m2sq)")
    return res
