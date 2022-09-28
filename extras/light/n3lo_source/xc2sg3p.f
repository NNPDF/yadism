*
* ..File: xc2sg3p.f    F_2^PS  and  F_2^G
*
*
* ..Parametrizations of the 3-loop MS(bar) pure-singlet and gluon coef-
*    ficient functions for the electromagnetic structure function F_2
*    at  mu_r = mu_f = Q. The expansion parameter is  alpha_s/(4 pi).
*
*  ..The relative accuracy of these parametrizations, as well as of
*    the convolution results, is one part in thousand or better.
*
* ..Reference: J. Vermaseren, A. Vogt and S. Moch 
*              hep-ph/0504242 = Nucl. Phys. B724 (2005) 3
* 
* =====================================================================
*
*
* ..The pure-singlet coefficient function, regular piece
*
       FUNCTION C2S3A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       DIMENSION FL(6), FLS(6)
       INTEGER NF
       DATA FL  / -1.d0, 0.5d0, 0.d0, 0.5d0, 0.2d0, 0.5d0 /
       DATA FLS /  1.d0, 0.1d0, 0.d0, 0.1d0, 0.018181818d0, 0.1d0 /
*
       DL  = LOG (Y)
       Y1  = 1.-Y
       DL1 = LOG (Y1)
       D9  = 1./9.D0
       D81 = D9*D9
*
       C2S31 = ( 856.*D81 * DL1**4 - 6032.*D81 * DL1**3 + 130.57* DL1**2
     ,         - 542.0 * DL1 + 8501. - 4714.* Y + 61.50 * Y**2 ) * Y1
     ,         + DL*DL1 * (8831.* DL + 4162.* Y1) - 15.44 * Y*DL**5     
     ,         + 3333.* Y*DL**2 + 1615.* DL + 1208.* DL**2 
     ,         - 333.73 * DL**3 + 4244.*D81 * DL**4 - 40.*D9 * DL**5 
     ,         - 2731.82 * Y1/Y - 414.262 * DL/Y
       C2S32 = ( - 64.*D81 * DL1**3 + 208.*D81 * DL1**2 + 23.09 * DL1
     ,         - 220.27 + 59.80 * Y - 177.6 * Y**2) * Y1 + 
     ,         -  DL*DL1 * (160.3 * DL + 135.4 * Y1) - 24.14 * Y*DL**3 
     ,         - 215.4 * Y*DL**2 - 209.8 * DL - 90.38 * DL**2 
     ,         - 3568./243.* DL**3 - 184.*D81 * DL**4 + 40.2426 * Y1/Y
       C2S3F = ( ( 126.42 - 50.29 * Y - 50.15 * Y**2) * Y1 - 26.717 
     ,         - 320.*D81 * DL**2 * (DL+5.D0) + 59.59 * DL 
     ,         - Y*DL**2 * (101.8 + 34.79 * DL + 3.070 * DL**2) 
     ,         - 9.075 * Y*Y1*DL1 ) * Y
       C2S3A = NF * ( C2S31 + (FLS(NF)-FL(NF)) * C2S3F + NF * C2S32 )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..The (truncated) 'local' piece due to the FL11 contribution
*
       FUNCTION C2S3C (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF
       DIMENSION FL(6), FLS(6)
       DATA FL  / -1.d0, 0.5d0, 0.d0, 0.5d0, 0.2d0, 0.5d0 /
       DATA FLS /  1.d0, 0.1d0, 0.d0, 0.1d0, 0.018181818d0, 0.1d0 /
*
       FL11 = FL(NF)
       C2S3C = - (FLS(NF)-FL(NF)) * NF * 11.8880
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..The gluon coefficient function
*
       FUNCTION C2G3A (Y, NF)
       IMPLICIT REAL*8 (A-Z)
       DIMENSION FLG(6)
       INTEGER NF
       DATA FLG / 1.d0, 0.1d0, 0.d0, 0.1d0, 0.018181818d0, 0.1d0 /
*
       YI  = 1./Y
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
       D9  = 1./9.D0
       D81 = D9*D9
*
       C2G31 = 
     ,           966.*D81 * DL1**5 - 935.5*D9 * DL1**4 + 89.31 * DL1**3 
     ,         + 979.2 * DL1**2 - 2405. * DL1 + 1372.* (1.-Y)* DL1**4
     ,         - 15729. - 310510.* Y + 331570.* Y**2 - 244150.* Y*DL**2
     ,         - 253.3* Y*DL**5
     ,         + DL*DL1 * (138230. - 237010.* DL) - 11860.* DL 
     ,         - 700.8 * DL**2 - 1440.* DL**3 + 2480.5*D81 * DL**4
     ,         - 134.*D9 * DL**5 - 6362.54 * YI - 932.089 * DL*YI
       C2G32 = 
     ,           131.*D81 * DL1**4 - 14.72 * DL1**3 + 3.607 * DL1**2
     ,         - 226.1 * DL1 + 4.762 - 190.0 * Y - 818.4 * Y**2
     ,         - 4019.* Y*DL**2 - DL*DL1 * (791.5 + 4646 * DL)
     ,         + 739.0 * DL + 418.0 * DL**2 + 104.3 * DL**3 
     ,         + 809.*D81 * DL**4 + 12.*D9 * DL**5 + 84.423 * YI
       C2G3F =   3.211 * DL1**2 + 19.04 * Y*DL1 + 0.623 * (1.-Y)*DL1**3 
     ,         - 64.47 * Y + 121.6 * Y**2 - 45.82 * Y**3 - Y*DL*DL1 
     ,         * ( 31.68 + 37.24 * DL) - Y*DL * (82.40 + 16.08 * DL)
     ,         + Y*DL**3 * (520.*D81 + 11.27 * Y) + 60.*D81 * Y*DL**4
       C2G3A = NF * ( C2G31 + NF * (C2G32 + FLG(NF) * C2G3F) )
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..The artificial 'local' piece, introduced to fine-tune the accuracy. 
*
       FUNCTION C2G3C (Y, NF)
       IMPLICIT REAL*8 (A - Z)
       INTEGER NF
*
       C2G3C = 0.625 * NF
*
       RETURN
       END
*
* =================================================================av==
