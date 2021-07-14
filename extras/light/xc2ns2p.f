*
* ..File: xc2ns2p.f    F2_NS
*
*
* ..Calculation of the 2-loop x-space MS(bar) coefficient functions
*    for F2 via compact parametrizations involving only logarithms.
*    Non-singlet, mu_r = mu_f = Q. Expansion parameter: alpha_s/(4 pi).
*
*  ..The distributions (in the mathematical sense) are given as in eq.
*    (B.26) of Floratos, Kounnas, Lacaze: Nucl. Phys. B192 (1981) 417.
*    The name-endings A, B, and C of the functions below correspond to
*    the kernel superscripts [2], [3], and [1] in that equation.
*
*  ..The relative accuracy of the coefficient functions, as well as of
*    the convolution results, amounts to a few thousandth.
*
*  ..Reference: W.L. van Neerven and A. Vogt,
*               hep-ph/9907472 = Nucl. Phys. B568 (2000) 263
*  ..The user should also cite the original calculation,
*     E.B. Zijlstra and W.L. van Neerven, Phys. Lett. B272 (1991) 127.
*
*
* =====================================================================
*
*
* ..This is the regular non-singlet piece for the electromagnetic F2,
*    corresponding to C2NSP+C2NSN in W. van Neerven's program. The
*    (10+8) numerical coefficients are fitted to his results, using x
*    values between 10^-6 and 1-10^-6.
*
       FUNCTION C2NN2A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2NN2A =
     1          - 69.59 - 1008.* Y
     2          - 2.835 * DL**3 - 17.08 * DL**2 + 5.986 * DL
     3          - 17.19 * DL1**3 + 71.08 * DL1**2 - 660.7 * DL1
     4          - 174.8 * DL * DL1**2 + 95.09 * DL**2 * DL1
     5        + NF * ( - 5.691 - 37.91 * Y
     6          + 2.244 * DL**2 + 5.770 * DL
     7          - 1.707 * DL1**2  + 22.95 * DL1
     8          + 3.036 * DL**2 * DL1 + 17.97 * DL * DL1 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the regular non-singlet piece for the odd-moment (CC) F2,
*    corresponding to C2NSP-C2NSN in WvN's program. For the NF^0 piece
*    8 numerical coefficients are fitted to his results, the ones of
*    ln^3(1-y) and ln^2(1-y) are taken over from C3NN2A. The NF piece
*    is also the same as in C3NN2A.
*
       FUNCTION C2NC2A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2NC2A =
     1          - 84.18 - 1010.* Y
     2          - 3.748 * DL**3 - 19.56 * DL**2 - 1.235 * DL
     3          - 17.19 * DL1**3 + 71.08 * DL1**2 - 663.0 * DL1
     4          - 192.4 * DL * DL1**2 + 80.41 * DL**2 * DL1
     5        + NF * ( - 5.691 - 37.91 * Y
     6          + 2.244 * DL**2 + 5.770 * DL
     7          - 1.707 * DL1**2  + 22.95 * DL1
     8          + 3.036 * DL**2 * DL1 + 17.97 * DL * DL1 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the singular NS piece, denoted by SOFT2 in WvN's program.
*    It is the same for all F2 and F3 cases. The numerical coefficients
*    are exact, but truncated.
*
       FUNCTION C2NS2B (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C2NS2B =
     1          + 14.2222 * DL1**3 - 61.3333 * DL1**2 - 31.105 * DL1
     2          + 188.64
     3        + NF * ( 1.77778 * DL1**2 - 8.5926 * DL1 + 6.3489 )
       C2NS2B = DM * C2NS2B
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' NS piece for the e.m. F2, denoted by COR2 in
*    WvN's program. The numerical coefficients of the logs are exact,
*    but truncated, the constant one (from the delta-function) is
*    slightly adjusted (+ 0.485 - 0.0035 NF) using the lowest moments.
*
       FUNCTION C2NN2C (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
*
       C2NN2C =
     1          + 3.55555 * DL1**4 - 20.4444 * DL1**3 - 15.5525 * DL1**2
     2          + 188.64 * DL1 - 338.531 + 0.485
     3        + NF * (0.592593 * DL1**3 - 4.2963 * DL1**2
     4          + 6.3489 * DL1 + 46.844 - 0.0035)
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' NS piece for the CC F2, also given by COR2 in
*    WvN's program. The numerical coefficients of the logs are exact,
*    but truncated, the constant one is adjusted (- 0.2652 - 0.0035 NF)
*    using the lowest moments.
*
       FUNCTION C2NC2C (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
*
       C2NC2C =
     1          + 3.55555 * DL1**4 - 20.4444 * DL1**3 - 15.5525 * DL1**2
     2          + 188.64 * DL1 - 338.531 + 0.537
     3        + NF * (0.592593 * DL1**3 - 4.2963 * DL1**2
     4          + 6.3489 * DL1 + 46.844 - 0.0035)
*
       RETURN
       END
*
* =================================================================av==
