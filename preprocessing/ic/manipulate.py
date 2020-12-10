# -*- coding: utf-8 -*-
from . import mma

translate = {
    1: "One",
    2: "Two",
    3: "Three",
}


def init_vars(runner, kind, fhat, M, N):
    fhat = mma.prepare(fhat)
    M = mma.prepare(M)
    N = mma.prepare(N)
    kind = translate[kind]
    code_vars = f"""f{kind}hat = {fhat};
    m{kind} = {M};
    n{kind} = {N};
    f{kind}hatJoined = (m{kind} / n{kind} * f{kind}hat) (*/. {{x -> xBj}}*);
    """
    return runner.send(code_vars)


def join_fl(runner):
    code_fhat = """fLhatJoined = f2hatJoined - 2*x*f1hatJoined;"""
    return runner.send(code_fhat)


def parse_reg(runner, kind, Spm):
    kind = translate[kind]
    code_fhat = f"""
    f{kind}coeff{Spm} = Coefficient[f{kind}hatJoined, {Spm}];
    f{kind}coeff{Spm} = f{kind}coeff{Spm} /. {{Ixi->(s1h+2m22)/(s1h^2) + (s1h+m22)/(Delp*s1h^2)*Spp*Lxi}};
    Print@FortranForm@Collect[f{kind}coeff{Spm},{{Lxi}}, FullSimplify];"""
    return runner.send(code_fhat)


def parse_soft(runner, kind, Spm):
    kind = translate[kind]
    code_hcoeff = f"""
    Print@Module[{{gcoeff}},
        gcoeff = zeroAt1 * s1h/(8*(s1h + m22)) * f{kind}coeff{Spm};
        gcoeff = gcoeff /. {{s1h -> zeroAt1 * s1hreg}};
        hcoeff = Limit[gcoeff,zeroAt1->0];
        hcoeff = hcoeff /. {{Delp -> Del, Lxi -> Lxisoft, s1hreg -> Del}};
        FortranForm@Collect[hcoeff,{{Lxi}},FullSimplify]
    ];"""
    return runner.send(code_hcoeff)


def post_process(res):
    # replace all variables
    res = res.replace("m12", "pc.m1sq").replace("m22", "pc.m2sq")
    res = (
        res.replace("Spp", "pc.sigma_pp")
        .replace("Spm", "pc.sigma_pm")
        .replace("Smp", "pc.sigma_mp")
    )
    res = res.replace("Del", "pc.delta")
    res = (
        res.replace("Lxi", "pc.L_xi")
        .replace("Ixi", "pc.I_xi")
        .replace("s1h", "pc.s1hat")
    )
    res = res.replace("Q2IC", "pc.ESF.Q2").replace("xBj", "pc.ESF.x")
    res = res.replace("m1*m2", "np.sqrt(pc.m1sq * pc.m2sq)")
    return res
