*                                           __
* ..File: xc3ns3p.f    odd-N based F3 (nu + nu charged-current)
*
*
* ..Parametrization of the 3-loop MS(bar) non-singlet coefficient
*    function for the structure function F_3 in charged-current DIS.
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
* ..Reference: S. Moch, J. Vermaseren and A. Vogt,
*              hep-ph/0608307  = NP B (Proc. Suppl.) 160 (2006) 44
*              arXiv:0812.4168 = Nucl. Phys. B813 (2009) 220
*
* =====================================================================
*
*
* ..The regular piece. The rational end-point coefficients are exact,
*    the rest has been fitted for x between 10^-6 and 1 - 10^-6.
*    For FL02 = 1(0) the fl02 flavour class is (not) taken into account
*
       FUNCTION C3NM3A (Y, NF, FL02)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF, FL02
*
       Y1  = 1.D0 -Y
       DL  = LOG (Y)
       DL1 = LOG (Y1)
       D27  = 1./27.D0
       D81  = 1./81.D0
       D243 = 1./243.D0
*
       C3NM3A =
     ,            - 1853. - 5709.* Y + Y*Y1* (5600. - 1432.* Y)
     ,            - 536./405.D0* DL**5 - 4036.*D81* DL**4
     ,            - 496.95 * DL**3 - 1488. * DL**2 - 293.3 * DL
     ,            - 512.*D27 * DL1**5 + 8896.*D27 * DL1**4
     ,            - 1396.* DL1**3 + 3990.* DL1**2 + 14363.* DL1
     ,            - 0.463 * Y*DL**6 - DL*DL1 * (4007. + 1312.*DL)
     ,        + NF * ( 516.1 - 465.2 * Y + Y*Y1* (635.3 + 310.4 * Y)
     ,            + 304.*D81 * DL**4 + 48512./729.D0 * DL**3
     ,            + 305.32 * DL**2 + 366.9 * DL - 1.200 * Y*DL**4
     ,            - 640.*D81 * DL1**4 + 32576.*D243* DL1**3
     ,            - 660.7 * DL1**2 + 959.1 * DL1 + 31.95 * (1.-Y)*DL1**4
     ,            + DL*DL1 * (1496. + 270.1 * DL - 1191.* DL1) )
     ,        + NF**2 * ( 11.32 + 51.94 * Y - Y*Y1* (44.52 + 11.05 * Y)
     ,            - 368.* D243* DL**3 - 2848.*D243* DL**2 - 16.00 * DL
     ,            - 64.*D81* DL1**3 + 992.*D81* DL1**2 - 49.65 * DL1
     ,            - DL*DL1 * ( 39.99 + 5.103 * DL - 16.30 * DL1)
     ,            + 0.0647 * Y*DL**4 )
     ,        + FL02*NF * ( 48.79 - (242.4 - 150.7 * Y ) * Y1
     ,           - 16.*D27* DL**5 + 17.26* DL**3 - 113.4 * DL**2
     ,           - 477.0 * DL + 2.147 * DL1**2 - 24.57 * DL1
     ,           + Y*DL * (218.1 + 82.27 * DL**2)
     ,           - DL*DL1 * (81.70 + 9.412 * DL1) ) * Y1
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..The exact singular piece (irrational coefficients truncated)
*
       FUNCTION C3NS3B (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
       D81 = 1./81.D0
*
       C3NS3B =
     ,            + 1536.*D81 * DL1**5 - 16320.* D81 * DL1**4
     ,            + 5.01099E+2 * DL1**3 + 1.17154E+3 * DL1**2
     ,            - 7.32845E+3 * DL1 + 4.44276E+3
     ,        + NF * ( 640.* D81 * DL1**4 - 6592.* D81 * DL1**3
     ,            + 220.573 * DL1**2 + 294.906 * DL1 - 729.359 )
     ,        + NF**2 * ( 64.* D81 * DL1**3 - 464.* D81 * DL1**2
     ,            + 7.67505 * DL1 + 1.00830 )
*
       C3NS3B = DM * C3NS3B
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
       FUNCTION C3NM3C (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF
*
       DL1 = LOG (1.-Y)
       D81 = 1./81.D0
       D3  = 1./3.D0
*
       C3NM3C =
     ,            + 256.*D81 * DL1**6 - 3264.*D81 * DL1**5
     ,            + 1.252745E+2 * DL1**4 + 3.905133E+2 * DL1**3
     ,            - 3.664225E+3 * DL1**2 + 4.44276E+3  * DL1
     ,            - 9195.48 + 22.80
     ,        + NF * ( 128.* D81 * DL1**5 - 1648.* D81 * DL1**4
     ,            + 220.573 * D3 * DL1**3 + 147.453 * DL1**2
     ,            - 729.359 * DL1 + 2575.074 + 0.386 )
     ,        + NF**2 * ( 16.* D81 * DL1**4 - 464.* D81*D3 * DL1**3
     ,            + 7.67505 * 5.D-1 * DL1**2 + 1.0083 * DL1 - 103.2521
     ,            - 0.0081 )
*
       RETURN
       END
*
* =================================================================av==
