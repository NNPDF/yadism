# -*- coding: utf-8 -*-
import re

# Translation table as MMa doesn't like numbers in names
translate = {1: "One", 2: "Two", 3: "Three", "L": "L"}


def prepare(fform, mma_mode=True):
    """
    Translate Fortran expressions to Mathematica.

    - remove line markers
    - remove float marker
    - remove inline squaring

    Parameters
    ----------
        fform : str
            Fortran expression
        mma_mode : bool
            replace ** with ^ as is suitable in MMa?

    Returns
    -------
        mform : str
            equivalent Mathematica expression
    """
    fform = re.sub("\n *\\d", "", fform)
    fform = fform.replace("d0", "")
    fform = fform.replace("s1h2", "s1h**2")
    fform = fform.replace("Del2", "Del**2")
    fform = fform.replace("Delp2", "Delp**2")
    if mma_mode:
        fform = fform.replace("**", "^")
    return fform


def init_kind_vars(runner, kind, fhat, M, N, V):
    r"""
    Init all variables that depend on the observable kind.

    Parameters
    ----------
        runner : MmaRunner
            Mathematica instance
        kind : str
            observable kind
        fhat : str
            MMa expression for :math:`\hat f_k`
        M : str
            MMa expression for the ratio between :math:`F_k` and :math:`\mathcal F_k`
        N : str
            MMa expression for :math:`N_k`
        V : str
            MMa expression for :math:`V_k`

    Returns
    -------
        ex : str
            MMa expression - should be empty!
    """
    fhat = prepare(fhat)
    M = prepare(M)
    N = prepare(N)
    V = prepare(V)
    kind = translate[kind]
    code_vars = f"""f{kind}hat = {fhat};
    m{kind} = {M};
    n{kind} = {N};
    v{kind} = {V};
    f{kind}hatJoined = (m{kind} / n{kind} * f{kind}hat);
    v{kind}Joined = m{kind} * v{kind};
    """
    return runner.send(code_vars)


def join_fl(runner):
    """
    Define expressions for :math:`F_L = F_2 - 2xF_1`.

    Parameters
    ----------
        runner : MmaRunner
            Mathematica instance

    Returns
    -------
        ex : str
            MMa expression - should be empty!
    """
    code = f"""
    fLhatJoined = f{translate[2]}hatJoined - 2*x*f{translate[1]}hatJoined;
    vLJoined = v{translate[2]}Joined - 2*x*v{translate[1]}Joined;
    """
    return runner.send(code)


def parse_reg(runner, kind, Spm):
    """
    Select a coupling coefficient and print the regular part

    Parameters
    ----------
        runner : MmaRunner
            Mathematica instance
        kind : str
            observable kind
        Spm : str
            coupling coefficient

    Returns
    -------
        ex : str
            MMa expression
    """
    kind = translate[kind]
    code_fhat = f"""
    f{kind}coeff{Spm} = Coefficient[f{kind}hatJoined, {Spm}];
    f{kind}coeff{Spm} = f{kind}coeff{Spm} /. {{Ixi->(s1h+2m22)/(s1h^2) + (s1h+m22)/(Delp*s1h^2)*Spp*Lxi}};
    Print@FortranForm@Collect[f{kind}coeff{Spm}/. {{x -> xBj, Del->delta}},{{Lxi}}, FullSimplify];"""
    return runner.send(code_fhat)


def parse_virt(runner, kind, Spm):
    """
    Select a coupling coefficient and print the virtual part.

    Parameters
    ----------
        runner : MmaRunner
            Mathematica instance
        kind : str
            observable kind
        Spm : str
            coupling coefficient

    Returns
    -------
        ex : str
            MMa expression
    """
    kind = translate[kind]
    code_fhat = f"""
    v{kind}coeff{Spm} = Coefficient[v{kind}Joined, {Spm}];
    Print@FortranForm@Collect[v{kind}coeff{Spm}/. {{x -> xBj, Del->delta}},{{Lxi}}, FullSimplify];
    """
    return runner.send(code_fhat)


def parse_soft(runner, kind, Spm):
    """
    Select a coupling coefficient and print the soft part,
    i.e. the z->1 limit of the regular part

    Parameters
    ----------
        runner : MmaRunner
            Mathematica instance
        kind : str
            observable kind
        Spm : str
            coupling coefficient

    Returns
    -------
        ex : str
            MMa expression
    """
    kind = translate[kind]
    code_hcoeff = f"""
    Print@Module[{{gcoeff}},
        gcoeff = zeroAt1 * s1h/(8*(s1h + m22)) * f{kind}coeff{Spm};
        gcoeff = gcoeff /. {{s1h -> zeroAt1 * s1hreg}};
        hcoeff = Limit[gcoeff,zeroAt1->0];
        hcoeff = hcoeff /. {{Delp -> Del, Lxi -> Lxisoft, s1hreg -> Del}};
        FortranForm@Collect[hcoeff/. {{x -> xBj, Del->delta}},{{Lxi}},FullSimplify]
    ];"""
    return runner.send(code_hcoeff)


def post_process(res):
    """
    Rewrite expressions to the external part.

    Parameters
    ----------
        res : str
            input expression

    Returns
    -------
        res : str
            improved expression
    """
    # replace all variables
    res = res.replace("m12", "pc.m1sq").replace("m22", "pc.m2sq")
    res = (
        res.replace("Spp", "pc.sigma_pp")
        .replace("Spm", "pc.sigma_pm")
        .replace("Smp", "pc.sigma_mp")
    )
    res = (
        res.replace("delta", "pc.delta")
        .replace("Delp", "pc.deltap")
        .replace("Del", "pc.delta")
    )
    res = (
        res.replace("Lxi", "pc.L_xi")
        .replace("Ixi", "pc.I_xi")
        .replace("s1h", "pc.s1hat")
    )
    res = res.replace("Q2IC", "pc.Q2").replace("xBj", "pc.x")
    res = re.sub(r"m1\s*\*\s*m2", "np.sqrt(pc.m1sq * pc.m2sq)", res)
    res = (
        res.replace("dlog", "np.log").replace("dabs", "np.abs").replace("ddilog", "li2")
    )
    res = (
        res.replace("CRm", "pc.CRm")
        .replace("C1m", "pc.C1m")
        .replace("C1p", "pc.C1p")
        .replace("Cplus", "pc.Cplus")
        .replace("I1", "pc.I1")
    )
    res = re.sub("\\s+", " ", res)
    return res
