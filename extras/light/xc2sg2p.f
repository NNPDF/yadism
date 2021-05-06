*
* ..File: xc2sg2p.f    F2_S
*
*
* ..Calculation of the 2-loop x-space MS(bar) coefficient functions 
*    for F2 via compact parametrizations involving only logarithms.
*    Singlet, mu_r = mu_f = Q. Expansion parameter: alpha_s/(4 pi).
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
*               hep-ph/0006154 = Nucl. Phys. B588 (2000) 345
*  ..The user should also cite the original calculations,
*     E.B. Zijlstra and W.L. van Neerven, Phys. Lett. B272 (1991) 127
*     (pure singlet) and Phys. Lett. B273 (1991) 476 (gluon).
*
* 
* =====================================================================
*
*
* ..This is the pure singlet piece, denoted by C2S in WvN's program. 
*    Seven numerical coefficients (all but the one of 1/y, which is 
*    exact up to truncation) are fitted to his results, using x values
*    between 10^-6 and 1-10^-6.
*
       FUNCTION C2S2A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2S2A =   NF * ( 5.290 * (1./Y-1.) + 4.310 * DL**3   
     1         - 2.086 * DL**2 + 39.78 * DL - 0.101 * (1.-Y) * DL1**3 
     2         - (24.75 - 13.80 * Y) * DL**2 * DL1 + 30.23 * DL * DL1 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the regular gluon piece, denoted by C2G2 in WvN's program. 
*    Nine numerical coefficients are fitted as above, the ones of 1/y, 
*    ln^3(1-y), and ln^2(1-y) are exact up to truncation.
*
       FUNCTION C2G2A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2G2A =   NF * ( 1./Y * (11.90 + 1494.* DL1) + 5.319 * DL**3  
     1         - 59.48 * DL**2 - 284.8 * DL + 392.4 - 1483.* DL1
     2         + (6.445 + 209.4 * (1.-Y)) * DL1**3 - 24.00 * DL1**2
     3         - 724.1 * DL**2 * DL1 - 871.8 * DL * DL1**2 )
*
       RETURN
       END
* 
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' gluon piece, which has no counterpart in WvN's
*    program, as it does not exist in the exact expressions. Here it 
*    is, however, relevant for achieving the highest accuracy of the 
*    convolution, as are the adjustments of the constant in the non-
*    singlet quark coefficient functions. The value is fixed from the 
*    lowest moments. 
*
       FUNCTION C2G2C (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       C2G2C = - NF * 0.28  
*
       RETURN
       END
*
* =================================================================av==
