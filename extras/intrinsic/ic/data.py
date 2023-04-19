"""
This contains all the Fortran expressions needed for IC as given by APFEL.
"""

f2hat = """16d0 / Delp**4 * ( - 2d0 * Del**4 * Splus * Ixi
     1     + 2d0 * m1 * m2 * Sminus * ( ( ( s1h + m22 ) / Delp )
     2     * ( Delp2 - 6d0 * m12 * Q2IC ) * Lxi
     3     - Delp2 * ( s1h + Spp ) / 2d0 / ( s1h + m22 )
     4     + ( 2d0 * Delp2 - 3d0 * Q2IC * ( s1h + Spp) ) )
     5     + Splus * ( - 2d0 * ( Del2 - 6d0 * m12 * Q2IC )
     6     * ( s1h + m22 ) - 2d0 * ( m12 + m22 ) * s1h2
     7     - 9d0 * m22 * Spm**2 + Del2 * ( 2d0 * Spp - m22 )
     8     + 2d0 * s1h * ( 2d0 * Del2 + ( m12 - 5d0 * m22 ) * Spm )
     9     + ( Delp2 - 6d0 * Q2IC * ( m22 + s1h ) )
     1     * Spp * ( s1h + Spp ) / 2d0 / ( s1h + m22 )
     2     - 2d0 * Del2 / s1h * ( Del2
     3     + 2d0 * ( 2d0 * m22 + s1h ) * Spm )
     4     + ( s1h + m22 ) / Delp * ( - 2d0 / s1h * Del2
     5     * ( Del2 + 2d0 * Spm * Spp )
     6     - 2d0 * s1h * ( Del2 - 6d0 * m12 * Q2IC )
     7     - ( Delp2 - 18d0 * m12 * Q2IC ) * Spp
     8     - 2d0 * Del2 * ( Spp + 2d0 * Spm) ) * Lxi ) )"""

f1hat = """8d0 / Delp2 * ( - Del2 * ( Splus * Spp
     1     - 2d0 * m1 * m2 * Sminus ) * Ixi
     2     + 2d0 * m1 * m2 * Sminus * ( 1d0 / s1h * ( Delp2
     3     + 4d0 * m22 * Spm )
     4     + 2d0 * Spm - Smp + (Spp + s1h) / 2d0
     5     + ( s1h + m22 ) / Delp / s1h * ( Delp2
     6     + 2d0 * Spm * Spp + ( m22 + Q2IC ) * s1h ) * Lxi )
     7     + Splus * ( ( - m22 * Spp ) / ( ( s1h + m22 ) * s1h )
     8     * ( Del2 + 4d0 * m22 * Spm)
     9     - 1d0 / 4d0 / ( s1h + m22 )
     1     * ( 3d0 * Spp**2 * Smp
     2     + 4d0 * m22 * (10d0 * Spp * Spm - Spm * Smp
     3     - m12 * Spp)
     4     + s1h * ( - 7d0 * Spp * Smp + 18d0 * Del2
     5     - 4d0 * m12 * ( 7d0 * Q2IC - 4 * m22
     6     + 7d0 * m12 ) )
     7     + 3d0 * s1h2 * ( Spm - 2d0 * m12 ) - s1h**3 )
     8     + ( s1h + m22 ) / 2d0 / Delp
     9     * ( - 2d0 / s1h * Spp * ( Del2 + 2d0 * Spm * Spp )
     1     + ( 4d0 * m12 * m22 - 7d0 * Spm * Spp )
     2     - 4d0 * Spm * s1h - s1h**2 ) * Lxi ) )"""

f3hat = """16d0 / Delp2 * ( - 2d0 * Del2 * Rplus * Ixi
     1     + 2d0 * m1 * m2 * Rminus * ( 1d0 - Smp / s1h + ( s1h + m22 )
     2     * ( s1h + Spm ) / Delp / s1h * Lxi )
     3     + Rplus * ( Smp - 3d0 * Spm - 2d0 / s1h * ( Del2
     4     + 2d0 * m22 * Spm ) - ( s1h - Smp ) * ( s1h + Spp ) / 2d0
     5     / ( s1h + m22 ) + ( s1h + m22 ) / Delp / s1h * ( - s1h2
     6     + 4d0 * ( m12 * Smp - Del2 ) - 3d0 * s1h * Spm ) * Lxi ) )"""

N1 = """( Splus * Spp - 2d0 * m1 * m2 * Sminus ) / 2d0 /  Del"""

N2 = """2d0 * Splus * Del / Delp2"""

N3 = """2d0 * Rplus / Delp"""

M1 = """(Splus * Spp - 2*m1*m2*Sminus)/(2*Del)"""

M2 = """Splus * Del * x / (Q2IC)"""

M3 = """x * Rplus"""

I1 = """dlog( ( Spp + Del ) / ( Spp - Del ) ) / Del"""

Cplus = """2d0 * m1 * m2 * I1"""

C1m = """- ( Spm * I1 + dlog( m12 / m22 ) ) / Q2IC"""

C1p = """- ( Smp * I1 - dlog( m12 / m22 ) ) / Q2IC"""

CRm = """( Del2 / 2d0 / Q2IC
     1     + Spp * ( 1d0 + dlog( Q2IC / Del ) ) ) * I1
     2     + ( m22 - m12 ) / 2d0 / Q2IC * dlog( m12 / m22 )
     3     - dlog( Q2IC / m12 ) - dlog( Q2IC / m22 ) - 4d0
     4     + Spp / Del * (
     5     + dlog( dabs( ( Del - Spm ) / 2d0 / Q2IC ) )**2 / 2d0
     6     + dlog( dabs( ( Del - Smp ) / 2d0 / Q2IC ) )**2 / 2d0
     7     - dlog( dabs( ( Del + Spm ) / 2d0 / Q2IC ) )**2 / 2d0
     8     - dlog( dabs( ( Del + Smp ) / 2d0 / Q2IC ) )**2 / 2d0
     9     - ddilog( ( Del - Spm ) / 2d0 / Del )
     1     - ddilog( ( Del - Smp ) / 2d0 / Del )
     2     + ddilog( ( Del + Spm ) / 2d0 / Del )
     3     + ddilog( ( Del + Smp ) / 2d0 / Del ) )"""

S = """2d0 + Spp / Del * ( Del * I1
     1     + ddilog( 2d0 * Del / ( Del - Spp ) )
     2     - ddilog( 2d0 * Del / ( Del + Spp ) ) )
     3     + dlog( Del2 / m22 / Q2IC ) * ( - 2d0 + Spp * I1 )"""

V1 = """CRm
     1     + ( Sminus * Spp - 2d0 * Splus * m1 * m2 )
     2     / ( Splus * Spp - 2d0 * Sminus * m1 * m2 ) * Cplus"""

V2 = """CRm + ( m12 * C1p + m22 * C1m ) / 2d0
     1     + Sminus / Splus * ( Cplus + m1 * m2 / 2d0
     2     * ( C1p + C1m ) )"""

V3 = """CRm + Rminus / Rplus * Cplus"""
