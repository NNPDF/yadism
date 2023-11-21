*
* ..File: xc2ns3p.f    F2_NS
*
*
* ..Parametrization of the 3-loop MS(bar) non-singlet coefficient
*    functions for the structure function F_2 in electromagnetic DIS.
*    at  mu_r = mu_f = Q.  The expansion parameter is  alpha_s/(4 pi).
*
* ..The distributions (in the mathematical sense) are given as in eq.
*    (B.26) of Floratos, Kounnas, Lacaze: Nucl. Phys. B192 (1981) 417.
*    The name-endings A, B, and C of the functions below correspond to
*    the kernel superscripts [2], [3], and [1] in that equation.
*
*  ..The relative accuracy of these parametrizations, as well as of
*    the convolution results, is one part in thousand or better.
*
* ..References: S. Moch, J. Vermaseren and A. Vogt, hep-ph/0209100
*               J. Vermaseren, A. Vogt and S. Moch, hep-ph/0504242
*
*
* =====================================================================
*
*
* ..The regular piece. The rational end-point coefficients are exact,
*    the rest has been fitted for x between 10^-6 and 1 - 10^-6.
*
       FUNCTION C2NP3A (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF
       DIMENSION FL(6)
       DATA FL / -1.d0, 0.5d0, 0.d0, 0.5d0, 0.2d0, 0.5d0 /
*
       FL11 = FL(NF)
*
       Y1  = 1.D0 -Y
       DL  = LOG (Y)
       DL1 = LOG (Y1)
       D27  = 1./27.D0
       D243 = 1./243.D0
*
       C2NP3A =
     ,            - 4926. + 7725.* Y + 57256.* Y**2 + 12898.* Y**3
     ,            - 32.*D27 * DL**5 - 8796.*D243 * DL**4 - 309.1 * DL**3
     ,            - 899.6 * DL**2 - 775.8 * DL + 4.719 * Y*DL**5
     ,            - 512.*D27 * DL1**5 + 6336.*D27 * DL1**4
     ,            - 3368.* DL1**3 - 2978.* DL1**2 + 18832.* DL1
     ,            - 56000.* (1.-Y)*DL1**2 - DL*DL1 * (6158. + 1836.*DL)
     ,        + NF * ( 831.6 - 6752.* Y - 2778.* Y**2
     ,            + 728.* D243 * DL**4 + 12224.* D243 * DL**3
     ,            + 187.3 * DL**2 + 275.6 * DL + 4.102 * Y*DL**4
     ,            - 1920.* D243 * DL1**4 + 153.5 * DL1**3
     ,            - 828.7 * DL1**2 - 501.1 * DL1 + 171.0 * (1.-Y)*DL1**4
     ,            + DL*DL1 * (4365. + 716.2 * DL - 5983.* DL1) )
     ,        + NF**2 * ( 129.2 * Y + 102.5 * Y**2 - 368.* D243 * DL**3
     ,            - 1984.* D243 * DL**2 - 8.042 * DL
     ,            - 192.* D243 * DL1**3 + 18.21 * DL1**2 - 19.09 * DL1
     ,            + DL*DL1 * ( - 96.07 - 12.46 * DL + 85.88 * DL1) )
     ,        + FL11*NF * ( ( 126.42 - 50.29 * Y - 50.15 * Y**2) * Y1
     ,           - 26.717 - 960.*D243 * DL**2 * (DL+5.D0) + 59.59 * DL
     ,           - Y*DL**2 * (101.8 + 34.79 * DL + 3.070 * DL**2)
     ,           - 9.075 * Y*Y1*DL1 ) * Y
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..The exact singular piece (irrational coefficients truncated)
*
       FUNCTION C2NS3B (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
       D81 = 1./81.D0
*
       C2NS3B =
     ,            + 1536.*D81 * DL1**5 - 16320.* D81 * DL1**4
     ,            + 5.01099E+2 * DL1**3 + 1.17154E+3 * DL1**2
     ,            - 7.32845E+3 * DL1 + 4.44276E+3
     ,        + NF * ( 640.* D81 * DL1**4 - 6592.* D81 * DL1**3
     ,            + 220.573 * DL1**2 + 294.906 * DL1 - 729.359 )
     ,        + NF**2 * ( 64.* D81 * DL1**3 - 464.* D81 * DL1**2
     ,            + 7.67505 * DL1 + 1.00830 )
*
       C2NS3B = DM * C2NS3B
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..The 'local' piece.  The coefficients of delta(1-x) have been
*    slightly shifted with respect to their (truncated) exact values.
*
       FUNCTION C2NP3C (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF
       DIMENSION FL(6)
       DATA FL / -1.d0, 0.5d0, 0.d0, 0.5d0, 0.2d0, 0.5d0 /
*
       FL11 = FL(NF)
*
       DL1 = LOG (1.-Y)
       D81 = 1./81.D0
       D3  = 1./3.D0
*
       C2NP3C =
     ,            + 256.*D81 * DL1**6 - 3264.*D81 * DL1**5
     ,            + 1.252745E+2 * DL1**4 + 3.905133E+2 * DL1**3
     ,            - 3.664225E+3 * DL1**2 + 4.44276E+3  * DL1
     ,            - 9195.48 + 25.10
     ,        + NF * ( 128.* D81 * DL1**5 - 1648.* D81 * DL1**4
     ,            + 220.573 * D3 * DL1**3 + 147.453 * DL1**2
     ,            - 729.359 * DL1 + 2575.074 - 0.387 )
     ,        + NF**2 * ( 16.* D81 * DL1**4 - 464.* D81*D3 * DL1**3
     ,            + 7.67505 * 5.D-1 * DL1**2 + 1.0083 * DL1 - 103.2521
     ,            + 0.0155 )
     ,        - FL11*NF * 11.8880
*
       RETURN
       END
*
* =================================================================av==
