*
* ..File: xk3cnvp.f    K2_NS, K3_NS
*
*
* ..Calculation of the convolutions c^(1)*c^(1) of the 1-loop quark
*    coefficient functions for F2 and xF3 via compact parametrizations 
*    involving only logarithms. These convolutions enter the evolution 
*    kernels K_2 and K_3 for the non-singlet structure functions at 
*    third order in a_s == alpha_s/(4 pi).
*
*  ..The distributions (in the mathematical sense) are given as in eq.
*    (B.26) of Floratos, Kounnas, Lacaze: Nucl. Phys. B192 (1981) 417.
*    The name-endings A, B, and C of the functions below correspond to 
*    the kernel superscripts [2], [3], and [1] in that equation.
*
*  ..The relative accuracy of the results amounts to a few thousandth.
*    
*  ..Reference: W.L. van Neerven and A. Vogt, 
*               hep-ph/0103123 = Nucl. Phys. B621 (2002) 413
*
* 
* =====================================================================
*
*
* ..This is the regular part of c_{q,2}^(1)*c_{q,2}^(1). 
*    The numerical coefficients are fitted to exact results, using 
*    x-values between 10^-6 and 0.999. 
*
       FUNCTION C2Q1SA (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C2Q1SA = 
     1          - 410.5 - 483.3 * Y
     2          - 1.230 * DL**3 + 9.466 * DL**2 + 32.45 * DL 
     3          - 26.51 * DL1**3 + 192.9 * DL1**2 + 198.2 * DL1
     4          + 113.0 * DL * DL1**2 
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the corresponding regular part of c_{q,3}^(1)*c_{q,3}^(1). 
*
       FUNCTION C3Q1SA (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL  = LOG (Y)
       DL1 = LOG (1.-Y)
*
       C3Q1SA = 
     1          - 335.7 - 305.3* Y
     2          - 1.198 * DL**3 + 3.054 * DL**2 + 65.54 * DL 
     3          - 27.09 * DL1**3 + 162.1 * DL1**2 + 248.0 * DL1
     4          + 91.79 * DL * DL1**2 
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the singular piece for both cases. 
*    The coefficients are exact, but truncated.
*
       FUNCTION C2Q1SB (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL1 = LOG (1.-Y)
       DM  = 1./(1.-Y)
*
       C2Q1SB = 
     1          + 28.4444 * DL1**3 - 64.D0 * DL1**2 - 283.157 * DL1 
     2          + 304.751 
       C2Q1SB = DM * C2Q1SB
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term of c_{q,2}^(1)*c_{q,2}^(1). 
*    The numerical coefficients are exact, but truncated. 
*
       FUNCTION C2Q1SC (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL1 = LOG (1.-Y)
*
       C2Q1SC = 
     1          + 7.1111 * DL1**4 - 21.3333 * DL1**3 - 141.579 * DL1**2
     2          + 304.751 * DL1 + 346.213
*
       RETURN
       END
*
* ---------------------------------------------------------------------
*
*
* ..This is the 'local' term of c_{q,3}^(1)*c_{q,3}^(1). 
*    The numerical coefficients of the logs are exact, but truncated; 
*    the constant term is slightly adjusted using the lowest moments.
*
       FUNCTION C3Q1SC (Y)
       IMPLICIT REAL*8 (A-Z)
*
       DL1 = LOG (1.-Y)
*
       C3Q1SC = 
     1          + 7.1111 * DL1**4 - 21.3333 * DL1**3 - 141.579 * DL1**2
     2          + 304.751 * DL1 + 345.993 
*
       RETURN
       END
*
* =================================================================av==
