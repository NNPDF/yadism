*
* ..File: xclns3p.f    FL_NS
*
*
* ..Parametrization of the third-order MS(bar) non-singlet coefficient 
*    functions for the structure function F_L in electromagnetic DIS.
*    mu_r = mu_f = Q.  The expansion parameter is  alpha_s/(4 pi).
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
*              hep-ph/0411112 = Phys. Lett. B606 (2005) 123
*
* =====================================================================
*
*
* ..This is the regular piece. The rational end-point coefficients are
*    exact, the rest has been fitted for x between 10^-6 and 1 - 10^-6.
*    The N_f^2 part is exact and requires the dilogarithm Li2(x).
*
       FUNCTION CLNP3A (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       COMPLEX*16 WGPLG	
       INTEGER NF
       DIMENSION FL(6)
       DATA FL / -1.d0, 0.5d0, 0.d0, 0.5d0, 0.2d0, 0.5d0 /
       PARAMETER ( Z2 = 1.6449 34066 84822 64365 D0 )
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
       D81 = 1./81.D0
*
       FL11 = FL(NF)
*
       CLNP3A =  - 2220.5 - 7884.* Y + 4168.* Y**2 
     ,           - 1280.*D81 *DL**3 - 7456./27.D0 * DL**2 - 1355.7 * DL
     ,           + 512./27D0 * DL1**4 - 177.40 * DL1**3 + 650.6 *DL1**2
     ,           - 2729.* DL1 + 208.3 * Y*DL**3 - DL1**3*(1.-Y)* (125.3
     ,           - 195.6 *DL1) - DL*DL1 * (844.7 * DL + 517.3 * DL1)
     ,        + NF * ( 408.4 - 9.345 * Y - 919.3 * Y**2 
     ,           + 1728.*D81 * DL**2 + 200.73 * DL - 1792.*D81* Y*DL**3 
     ,           + 1024.*D81 * DL1**3 - 112.35 * DL1**2 + 344.1 * DL1
     ,           + (1.-Y)*DL1**2 * (239.7 + 20.63 * DL1)
     ,           + DL*DL1 * (887.3 + 294.5 * DL - 59.14 * DL1) )
     ,        + NF**2 * ( - 19. + (317./6.D0 - 12.*Z2) * Y 
     ,           + 9.* Y*DL**2 + DL * (-6. + 50.* Y)
     ,           + 3.* Y*DL1**2 + DL1 * (6. - 25.* Y) 
     ,           - 6.* Y*DL*DL1 + 6.* Y* LI2(Y) ) * 64.* D81
     ,        + FL11*NF * ( (107.0 + 321.05 * Y - 54.62 * Y**2) *(1.-Y)
     ,           - 26.717 - 320*D81 * DL**3 - 640.*D81 * DL**2 
     ,           + 9.773 * DL + Y*DL * (363.8 + 68.32 * DL) ) * Y
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' piece, introduced to fine-tune the accuracy.
*
       FUNCTION CLNP3C (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF
*
       CLNP3C = 0.113 + NF * 0.006
*
       RETURN
       END
*
* =================================================================av==
