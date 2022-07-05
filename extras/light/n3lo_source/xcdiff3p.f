*
* ..File: xcdiff3p.f    F_{i,NS},  i = 2,3,L  (even-N - odd-N)
*
*
* ..Parametrizations of the differences between the even-N and odd-N
*    based three-loop coefficient functions for the structure functions
*    F_L, F_2 and F_3 in charged-current deep-inelastic scattering.
*    MS(bar) scheme, the expansion parameter is  a_s = alpha_s/(4 pi).
*
* ..Except where the values are very small, the relative accuracy of
*     these parametrizations, as well as of the convolution results,
*     is one part in thousand or better.
*
* ..These functions should be used together with the results for the
*    even-N based F_L, F_2 and the odd-N F_3 respectively presented in
*              S. Moch, J. Vermaseren and A. Vogt,
*              hep-ph/0411112, hep-ph/0504242 and arXiv:0812.4168
*    For F_2 and F_L the (NC) flavour class fl11 has to be deactivated
*    there, and for F_3 the fl02 contributions have to be left out.
*
* ..Reference: J. Davies, S. Moch, J. Vermaseren and A. Vogt,
*              arXiv:1606.xxxxx
*
* =====================================================================
*
*
* ..F_2: third-order c_2^{nu+nubar} - c_2^{nu-nubar}
*
       FUNCTION c2q3dfP (Y, NF)
*
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       Y1  = 1.- Y
       DL  = LOG (Y)
       DL1 = LOG (Y1)
*
       C2Q30 =   273.59 - 44.95* Y - 73.56* Y**2 + 40.68* Y**3
     ,         + 0.1356* DL**5 + 8.483* DL**4 + 55.90* DL**3
     ,         + 120.67* DL**2 + 388.0* DL - 329.8* DL*DL1
     ,         - Y*DL* (316.2 + 71.63* DL) + 46.30*DL1 + 5.447* DL1**2
*
       C2Q31 = - 19.093 + 12.97* Y + 36.44* Y**2 - 29.256* Y**3
     ,         - 0.76* DL**4 - 5.317* DL**3 - 19.82* DL**2 - 38.958* DL
     ,         - 13.395* DL*DL1 + Y*DL* (14.44 + 17.74*DL) + 1.395* DL1
*
       c2q3dfP = (C2Q30 + NF * C2Q31)* Y1
*
       RETURN
       END
*
* ..The `local' piece for F2, artificial but useful for maximal accuracy
*    of moments and convolutions
*
       FUNCTION c2q3dfPC (Y, NF)
*
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       c2q3dfPC = - 0.0008 + 0.0001* NF
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
* ..F_L: third-order c_L^{nu+nubar} - c_L^{nu-nubar}
*
       FUNCTION cLq3dfP (Y, NF)
*
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       Y1  = 1.- Y
       DL  = LOG (Y)
       DL1 = LOG (Y1)
*
       CLQ30 = - 620.53 - 394.5* Y + 1609.* Y**2 - 596.2* Y**3
     ,         + 0.217* DL**3 + 62.18* DL**2 + 208.47* DL
     ,         - 482.5* DL*DL1 - Y*DL* (1751. - 197.5* DL)
     ,         + 105.5* DL1 + 0.442* DL1**2
*
       CLQ31 = - 6.500 - 12.435* Y + 23.66* Y**2 + 0.914* Y**3
     ,         + 0.015* DL**3 - 6.627* DL**2 - 31.91* DL
     ,         - Y*DL* (5.711 + 28.635* DL)
*
       cLq3dfP = (CLQ30 + NF * CLQ31) * Y1**2
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
* ..F_3: third-order c_3^{nu-nubar} - c_3^{nu+nubar}    Note the sign!
*
       FUNCTION c3q3dfP (Y, NF)
*
       IMPLICIT REAL*8 (A-Z)
       INTEGER IMOD, NF
*
       Y1  = 1.- Y
       DL  = LOG (Y)
       DL1 = LOG (Y1)
*
       C3Q30 = - 553.5 + 1412.5* Y - 990.3* Y**2 + 361.1* Y**3
     ,         + 0.1458* DL**5 + 9.688* DL**4 + 90.62* DL**3
     ,         + 83.684* DL**2 - 602.32* DL
     ,         - 382.5* DL*DL1 - Y*DL* (2.805 + 325.92* DL)
     ,         + 133.5* DL1 + 10.135* DL1**2
*
       C3Q31 = - 16.777 + 77.78* Y - 24.81* Y**2 - 28.89* Y**3
     ,         - 0.7714* DL**4 - 7.701* DL**3 - 21.522* DL**2
     ,         - 7.897* DL - 16.17* DL*DL1 + Y*DL* (43.21 + 67.04*DL)
     ,         + 1.519* DL1
*
       c3q3dfP = (C3Q30 + NF * C3Q31)* Y1
*
       RETURN
       END
*
* ..The `local' piece for F3 - present for the same reason as for F2
*
       FUNCTION c3q3dfPC (Y, NF)
*
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       c3q3dfPC = - 0.0029 + 0.00006* NF
*
       RETURN
       END
*
* =================================================================av==
