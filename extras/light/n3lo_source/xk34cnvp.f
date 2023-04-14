*
* ..File: xk34cnvp.f    K3_NS
*
*
* ..Calculation of the convolutions c^(1)*c^(1)*c^(1) and c^(2)*c^(1)
*    of the 1- and 2-loop coefficient functions for the non-singlet
*    structure function F_3 via compact parametrisations involving only
*    logarithms.  These convolutions enter the physical evolution
*    kernels K_3 for F_3^(+-) at fourth order in a_s == alpha_s/(4 pi).
*
*  ..The distributions (in the mathematical sense) are given as in eq.
*    (B.26) of Floratos, Kounnas, Lacaze: Nucl. Phys. B192 (1981) 417.
*    The name-endings A, B, and C of the functions below correspond to
*    the kernel superscripts [2], [3], and [1] in that equation.
*
*  ..The numerical coefficients of the regular parts (`A') are fitted
*     to the exact results (obtained via Mellin inversion) for x-values
*     between 10^-6 and 0.999. Those of the singulat pieces (`B'), as
*     well as the logarithmic terms of the `local' terms (`C') are
*     exact up to truncation. The constant terms in `C' are slightly
*     adjusted using the lowest integer moments. The relative accuracy
*     of the results amounts to a few per mille.
*
*  ..Reference: W.L. van Neerven and A. Vogt,
*               hep-ph/0103123 = Nucl. Phys. B621 (2002) 413
*
*
* =====================================================================
*
*
* ..This is the regular part of c_{q,3}^(1)*c_{q,3}^(1)*c_{q,3}^(1).
*
       FUNCTION C3Q1TA (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C3Q1TA =
     1          + 15890. + 15410.* Y
     2          - 0.119 * DL**5  + 3.126 * DL**4  + 84.84 * DL**3
     3          + 288.7 * DL**2  + 264.87 * DL
     4          - 138.4 * DL1**5 + 409.0 * DL1**4 - 1479. * DL1**3
     3          - 24700.* DL1**2 + 9646. * DL1
     4          - 10080. * DL * DL1**2
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the corresponding singular piece.
*
       FUNCTION C3Q1TB (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C3Q1TB =
     1          + 113.7778 * DL1**5 - 426.6667 * DL1**4
     2          - 2757.883 * DL1**3 + 9900.585 * DL1**2
     3          + 3917.516 * DL1 - 12573.13
       C3Q1TB = DM * C3Q1TB
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term for c_{q,3}^(1)*c_{q,3}^(1)*c_{q,3}^(1).
*
       FUNCTION C3Q1TC (Y)
       IMPLICIT REAL*8 (A-Z)

       DL1 = LOG (1.-Y)
       YM  = (1.-Y)
*
       C3Q1TC =
     1          + 113.7778/6.D0 * DL1**6 - 426.6667/5.D0 * DL1**5
     2          - 2757.883/4.D0 * DL1**4 + 9900.585/3.D0 * DL1**3
     3          + 3917.516/2.D0 * DL1**2 - 12573.13 * DL1 - 2888.1
*
       RETURN
       END
*
* =====================================================================
*
*
* ..This is the regular part of c_{NS,3}^(2+) * c_{q,3}^(1).
*
       FUNCTION C3Q12PA (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C3Q12PA =
     1          + 3349. + 22220. * Y
     2          - 0.404 * DL**5  - 5.525 * DL**4  + 23.80 * DL**3
     3          + 484.7 * DL**2  + 1577. * DL
     4          - 77.39 * DL1**5 + 295.5 * DL1**4 - 2587. * DL1**3
     5          - 10580.* DL1**2 + 30580.* DL1
     6          + 6461. * DL * DL1**2
     7   + NF * ( 468.0 - 891.9 * Y
     8          + 0.482 * DL**4 + 2.541 * DL**3 - 41.04 * DL**2
     9          - 223.9 * DL
     T          - 14.30 * DL1**4 + 10.47 * DL1**3
     1          - 775.2 * DL1**2 - 2458. * DL1
     2          - 392.9 * DL * DL1**2 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the regular part of c_{NS,3}^(2-) * c_{q,3}^(1).
*
       FUNCTION C3Q12MA (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C3Q12MA =
     1          + 2548. + 20080. * Y
     2          - 0.524 * DL**5  - 6.104 * DL**4  + 39.23 * DL**3
     3          + 553.5 * DL**2  + 1393. * DL
     4          - 77.39 * DL1**5 + 289.1 * DL1**4 - 2823. * DL1**3
     5          - 12500.* DL1**2 + 25420. * DL1
     6          + 9515.* DL * DL1**2
     7   + NF * ( 468.0 - 891.9 * Y
     8          + 0.482 * DL**4 + 2.541 * DL**3 - 41.04 * DL**2
     9          - 223.9 * DL
     T          - 14.30 * DL1**4 + 10.47 * DL1**3
     1          - 775.2 * DL1**2 - 2458. * DL1
     2          - 392.9 * DL * DL1**2 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the singular piece for both c^(2)*c^(1) cases.
*
       FUNCTION C3Q12B (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C3Q12B =
     1          + 56.8888 * DL1**5 - 343.702 * DL1**4 - 633.29 * DL1**3
     2          + 5958.86 * DL1**2 - 6805.10 * DL1 - 2464.47
     3    + NF * ( 7.9012 * DL1**4 - 55.3087 * DL1**3
     4          + 18.629 * DL1**2 + 619.865 * DL1 - 584.260 )
       C3Q12B = DM * C3Q12B
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term for c_{NS,3}^(2+) * c_{q,3}^(1).
*
       FUNCTION C3Q12PC (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
       DL1 = LOG (1.-Y)
*
       C3Q12PC =
     1         + 56.8888/6.D0 * DL1**6 - 343.702/5.D0 * DL1**5
     2         - 633.290/4.D0 * DL1**4 + 5958.86/3.D0 * DL1**3
     3         - 6805.10/2.D0 * DL1**2 - 2464.47 * DL1 + 8485.0
     4   + NF * ( 7.9012/5.D0 * DL1**5 - 55.3087/4.D0 * DL1**4
     2          + 18.629/3.D0 * DL1**3 + 619.865/2.D0 * DL1**2
     3          - 584.260 * DL1 - 803.43 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term for c_{NS,3}^(2-) * c_{q,3}^(1).
*
       FUNCTION C3Q12MC (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF

       DL1 = LOG (1.-Y)
*
       C3Q12MC =
     1         + 56.8888/6.D0 * DL1**6 - 343.702/5.D0 * DL1**5
     2         - 633.290/4.D0 * DL1**4 + 5958.86/3.D0 * DL1**3
     3         - 6805.10/2.D0 * DL1**2 - 2464.47 * DL1 + 8478.2
     4   + NF * ( 7.9012/5.D0 * DL1**5 - 55.3087/4.D0 * DL1**4
     2          + 18.629/3.D0 * DL1**3 + 619.865/2.D0 * DL1**2
     3          - 584.260 * DL1 - 803.43 )
*
       RETURN
       END
*
* =================================================================av==
