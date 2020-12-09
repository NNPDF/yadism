import re
import subprocess
import io
import sympy
import black
from sympy.parsing.sympy_parser import parse_expr

f2 = """16d0 / Delp**4 * ( - 2d0 * Del**4 * Splus * Ixi
     1     + 2d0 * m1 * m2 * Sminus * ( ( ( s1h + m22 ) / Delp )
     2     * ( Delp2 - 6d0 * m12 * Q2IC ) * Lxi
     3     - Delp2 * ( s1h + Spp ) / 2d0 / ( s1h + m22 )
     4     + ( 2d0 * Delp2 - 3d0 * Q2IC * ( s1h + Spp) ) )
     5     + Splus * ( - 2d0 * ( Del2 - 6d0 * m12 * Q2IC )
     6     * ( s1h + m22 ) - 2d0 * ( m12 + m22 ) * s1h2
     7     - 9d0 * m22 * Spm**2 + Del2 * ( 2d0 * Spp - m22 )
     8     + 2d0 * s1h * ( 2d0 * Del2 + ( m12 - 5d0 * m22 ) * Spm )
     9     + ( Delp2 - 6d0 * Q2IC * ( m22 + s1h ) )
     1     * Spp * ( s1h + Spp ) / 2d0 / ( s1h + m22 )
     2     - 2d0 * Del2 / s1h * ( Del2
     3     + 2d0 * ( 2d0 * m22 + s1h ) * Spm )
     4     + ( s1h + m22 ) / Delp * ( - 2d0 / s1h * Del2
     5     * ( Del2 + 2d0 * Spm * Spp )
     6     - 2d0 * s1h * ( Del2 - 6d0 * m12 * Q2IC )
     7     - ( Delp2 - 18d0 * m12 * Q2IC ) * Spp
     8     - 2d0 * Del2 * ( Spp + 2d0 * Spm) ) * Lxi ) )"""


def prepare(fform):
    fform = re.sub("\n *\\d", "", fform)
    fform = fform.replace("d0", "")
    fform = fform.replace("s1h2", "s1h**2")
    fform = fform.replace("Del2", "Del**2")
    fform = fform.replace("Delp2", "Delp**2")
    return fform


# fform = fform.replace("**","^")
# print(fform)
# print()


def parse(fform, Spm):
    ex = parse_expr(fform)
    ex = ex.expand().coeff(sympy.S(Spm)).expand()
    s = str(ex)
    s = s.replace("**", "^")
    # p = subprocess.Popen(["math", "-noprompt"], stdin=subprocess.PIPE,stdout=subprocess.PIPE)
    # p.communicate(input=f"t = {s};\nFortranForm@Collect[t,Lxi,FullSimplify]")
    with open("test.m", "w") as o:
        o.write(f"t = {s};\nFortranForm@Collect[t,Lxi,FullSimplify]")
    with open("test.m") as o:
        p = subprocess.run(["math", "-noprompt"], stdin=o, capture_output=True)
    res = p.stdout.decode()
    res = res.replace("\n", "")
    return res


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

    res = black.format_str(res, mode=black.FileMode())
    return res


print(post_process(parse(prepare(f2), "Sminus")))
