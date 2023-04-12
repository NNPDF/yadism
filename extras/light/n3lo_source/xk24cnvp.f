*
* ..File: xk24cnvp.f    K2_NS
*
*
* ..Calculation of the convolutions c^(1)*c^(1)*c^(1) and c^(2)*c^(1)
*    of the 1- and 2-loop non-singlet coefficient functions for F_2 
*    via compact parametrisations involving only logarithms.  These 
*    convolutions enter the evolution kernels K_2 for the structure 
*    functions F_{2,NS}^(+-) at fourth order in a_s == alpha_s/(4 pi).
*
*  ..The distributions (in the mathematical sense) are given as in eq.
*    (B.26) of Floratos, Kounnas, Lacaze: Nucl. Phys. B192 (1981) 417.
*    The name-endings A, B, and C of the functions below correspond to 
*    the kernel superscripts [2], [3], and [1] in that equation.
*
*  ..The numerical coefficients of the regular parts (`A') are fitted
*     to the exact results (obtained via Mellin inversion) for x-values
*     between 10^-6 and 0.999.  Those of the singulat pieces (`B'), as 
*     well as the logarithmic terms of the `local' terms (`C') are 
*     exact up to truncation.  The constant terms in `C' are slightly
*     adjusted using the lowest integer moments.  The relative accuracy
*     of the results amounts to a few thousandth.
*    
*  ..Reference: W.L. van Neerven and A. Vogt, 
*               hep-ph/0103123 = Nucl. Phys. B621 (2002) 413
*
* 
* =====================================================================
*
*
* ..This is the regular part of c_{q,2}^(1)*c_{q,2}^(1)*c_{q,2}^(1). 
*
       FUNCTION C2Q1TA (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2Q1TA = 
     1          + 8547. + 3618.* Y
     2          - 0.35  * DL**5 - 4.30  * DL**4 - 106.7 * DL**3 
     3          - 1257. * DL**2 - 4345. * DL 
     4          - 151.4 * DL1**5 + 118.9 * DL1**4 - 6155. * DL1**3
     3          - 47990.* DL1**2 - 30080. * DL1
     4          + 6423.* DL * DL1**2 
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the corresponding singular piece. 
*
       FUNCTION C2Q1TB (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C2Q1TB = 
     1          + 113.7778 * DL1**5 - 426.6667 * DL1**4
     2          - 2757.883 * DL1**3 + 9900.585 * DL1**2 
     3          + 3917.516 * DL1 - 12573.13
       C2Q1TB = DM * C2Q1TB
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term for c_{q,2}^(1)*c_{q,2}^(1)*c_{q,2}^(1). 
*
       FUNCTION C2Q1TC (Y)
       IMPLICIT REAL*8 (A-Z)

       DL1 = LOG (1.-Y)
       YM  = (1.-Y)
*
       C2Q1TC = 
     1          + 113.7778/6.D0 * DL1**6 - 426.6667/5.D0 * DL1**5
     2          - 2757.883/4.D0 * DL1**4 + 9900.585/3.D0 * DL1**3 
     3          + 3917.516/2.D0 * DL1**2 - 12573.13 * DL1 - 2851.0
* 
       RETURN
       END
*
* =====================================================================
*
*
* ..This is the regular part of c_{NS,2}^(2+) * c_{q,2}^(1).
*
       FUNCTION C2Q12PA (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2Q12PA = 
     1          + 6286. - 1251. * Y
     2          - 0.35  * DL**5  + 0.64  * DL**4  + 92.93 * DL**3 
     3          + 761.9 * DL**2  + 2450. * DL 
     4          - 101.7 * DL1**5 - 155.1 * DL1**4 - 6553. * DL1**3
     5          - 23590.* DL1**2 + 10620.* DL1
     6          + 9290. * DL * DL1**2
     7   + NF * ( 522.4 - 295.1 * Y
     8          + 0.48  * DL**4 - 1.08 * DL**3 - 43.83 * DL**2
     9          - 125.5 * DL
     T          - 11.71 * DL1**4 + 60.82 * DL1**3
     1          - 618.0 * DL1**2 - 1979. * DL1
     2          - 919.6 * DL * DL1**2 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the regular part of c_{NS,2}^(2-) * c_{q,2}^(1). 
*
       FUNCTION C2Q12MA (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2Q12MA = 
     1          + 6298. - 711.6 * Y
     2          - 0.45  * DL**5  + 1.80  * DL**4  + 114.0 * DL**3 
     3          + 856.6 * DL**2  + 2602. * DL 
     4          - 109.2 * DL1**5 - 243.4 * DL1**4 - 6890. * DL1**3
     5          - 24000.* DL1**2 + 10840.* DL1
     6          + 9144. * DL * DL1**2 
     7   + NF * ( 522.4 - 295.1 * Y
     8          + 0.48  * DL**4 - 1.08 * DL**3 - 43.83 * DL**2
     9          - 125.5 * DL
     T          - 11.71 * DL1**4 + 60.82 * DL1**3
     1          - 618.0 * DL1**2 - 1979. * DL1
     2          - 919.6 * DL * DL1**2 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the singular piece for both c^(2)*c^(1) cases. 
*
       FUNCTION C2Q12B (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C2Q12B = 
     1          + 56.8888 * DL1**5 - 343.702 * DL1**4 - 633.29 * DL1**3
     2          + 5958.86 * DL1**2 - 6805.10 * DL1 - 2464.47
     3    + NF * ( 7.9012 * DL1**4 - 55.3087 * DL1**3
     4          + 18.629 * DL1**2 + 619.865 * DL1 - 584.260 )
       C2Q12B = DM * C2Q12B
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term for c_{NS,2}^(2+) * c_{q,2}^(1). 
*
       FUNCTION C2Q12PC (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF

       DL1 = LOG (1.-Y)
*
       C2Q12PC = 
     1         + 56.8888/6.D0 * DL1**6 - 343.702/5.D0 * DL1**5 
     2         - 633.290/4.D0 * DL1**4 + 5958.86/3.D0 * DL1**3  
     3         - 6805.10/2.D0 * DL1**2 - 2464.47 * DL1 + 8609.2 
     4   + NF * ( 7.9012/5.D0 * DL1**5 - 55.3087/4.D0 * DL1**4
     2          + 18.629/3.D0 * DL1**3 + 619.865/2.D0 * DL1**2
     3          - 584.260 * DL1 - 809.14 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term for c_{NS,2}^(2-) * c_{q,2}^(1). 
*
       FUNCTION C2Q12MC (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF

       DL1 = LOG (1.-Y)
*
       C2Q12MC = 
     1         + 56.8888/6.D0 * DL1**6 - 343.702/5.D0 * DL1**5 
     2         - 633.290/4.D0 * DL1**4 + 5958.86/3.D0 * DL1**3  
     3         - 6805.10/2.D0 * DL1**2 - 2464.47 * DL1 + 8569.2
     4   + NF * ( 7.9012/5.D0 * DL1**5 - 55.3087/4.D0 * DL1**4
     2          + 18.629/3.D0 * DL1**3 + 619.865/2.D0 * DL1**2
     3          - 584.260 * DL1 - 809.14 )
*
       RETURN
       END
*
* =================================================================av==
