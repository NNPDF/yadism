*
* ..File: xc3ns2p.f    F3_NS
*
*
* ..Calculation of the 2-loop x-space MS(bar) coefficient functions 
*    for xF3 via compact parametrizations involving only logarithms.
*    mu_r = mu_f = Q. Expansion parameter: alpha_s/(4 pi).
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
*     E.B. Zijlstra and W.L. van Neerven, Phys. Lett. B297 (1992) 377.
*
* 
* =====================================================================
*
*                                                               __
* ..This is the regular non-singlet piece for the sum F3(nu)+F3(nu), 
*    corresponding to C3NSP-C3NSN in W. van Neerven's program. The 
*    (9+8) numerical coefficients are fitted to his results, using x 
*    values between 10^-6 and 1-10^-6. 
*
       FUNCTION C3NM2A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C3NM2A = 
     1          - 206.1 - 576.8 * Y
     2          - 3.922 * DL**3 - 33.31 * DL**2 - 67.60 * DL 
     3          - 15.20 * DL1**3 + 94.61 * DL1**2 - 409.6 * DL1
     4          - 147.9 * DL * DL1**2 
     5        + NF * ( - 6.337 - 14.97 * Y 
     6          + 2.207 * DL**2 + 8.683 * DL 
     7          + 0.042 * DL1**3 - 0.808 * DL1**2 + 25.00 * DL1
     8          + 9.684 * DL * DL1 )     
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*                                                                 __
* ..This is the regular non-singlet piece for the diff. F3(nu)-F3(nu), 
*    corresponding to C3NSP+C3NSN in WvN's program. For the NF^0 piece
*    7 numerical coefficients are fitted to his results, the ones of
*    ln^3(1-y) and ln^2(1-y) are taken over from C3NM2A. The NF piece
*    is also the same as in C3NM2A.
*
       FUNCTION C3NP2A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C3NP2A = 
     1          - 242.9 - 467.2 * Y
     2          - 3.049 * DL**3 - 30.14 * DL**2 - 79.14 * DL 
     3          - 15.20 * DL1**3 + 94.61 * DL1**2 - 396.1 * DL1
     4          - 92.43 * DL * DL1**2 
     5        + NF * ( - 6.337 - 14.97 * Y 
     6          + 2.207 * DL**2 + 8.683 * DL 
     7          + 0.042 * DL1**3 - 0.808 * DL1**2  + 25.00 * DL1
     8          + 9.684 * DL * DL1 )     
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
       FUNCTION C3NS2B (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C3NS2B = 
     1          + 14.2222 * DL1**3 - 61.3333 * DL1**2 - 31.105 * DL1 
     2          + 188.64 
     3        + NF * ( 1.77778 * DL1**2 - 8.5926 * DL1 + 6.3489 ) 
       C3NS2B = DM * C3NS2B
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*                                        __
* ..This is the 'local' NS piece for the nu+nu F3, denoted by COR2 in 
*    WvN's program. The numerical coefficients of the logs are exact,
*    but truncated, the constant one (from the delta-function) is 
*    slightly adjusted (- 0.104 + 0.013 NF) using the lowest moments.
*
       FUNCTION C3NM2C (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
*
       C3NM2C = 
     1          + 3.55555 * DL1**4 - 20.4444 * DL1**3 - 15.5525 * DL1**2
     2          + 188.64 * DL1 - 338.531 - 0.104 
     3        + NF * (0.592593 * DL1**3 - 4.2963 * DL1**2 
     4          + 6.3489 * DL1 + 46.844 + 0.013)
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*                                        __
* ..This is the 'local' NS piece for the nu-nu F3, also given by COR2 in
*    WvN's program. The numerical coefficients of the logs are exact,
*    but truncated, the constant one (from the delta-function) is 
*    slightly adjusted (- 0.152 + 0.013 NF) using the lowest moments.
*
       FUNCTION C3NP2C (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
*
       C3NP2C = 
     1          + 3.55555 * DL1**4 - 20.4444 * DL1**3 - 15.5525 * DL1**2
     2          + 188.64 * DL1 - 338.531  - 0.152 
     3        + NF * (0.592593 * DL1**3 - 4.2963 * DL1**2 
     4          + 6.3489 * DL1 + 46.844 + 0.013)
*
       RETURN
       END
*
* =================================================================av==
