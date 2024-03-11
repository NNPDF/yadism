# auto-generated module by fonll_nc_nnlo package
# pylint: skip-file
# fmt: off
import numba as nb
import numpy as np
from eko.constants import CA as ca
from eko.constants import CF as cf
from eko.constants import TR as tr

from ..special.nielsen import nielsen
from ..special.zeta import zeta2, zeta3


@nb.njit("f8(i8,i8,f8)", cache=True)
def wgplg(m,n,z):
    return nielsen(m,n,z).real

@nb.njit("f8(f8)", cache=True)
def clg1am0_a0(x):
    res = tr * 16e0 * x * ( 1e0 - x )
    return res

@nb.njit("f8(f8)", cache=True)
def c2g1am0_aq(x):
    res = tr * ( 4e0 - 8e0 * x + 8e0 * x**2 )
    return res

@nb.njit("f8(f8)", cache=True)
def c2g1am0_a0(x):
    res = tr * ( ( 4e0 - 8e0 * x + 8e0 * x**2 ) * np.log( ( 1e0 - x ) / x ) - 4e0 + 32e0 * x - 32e0 * x**2 )
    return res

@nb.njit("f8(f8)", cache=True)
def clg2am0_af(x):
    dlx=np.log(x)
    dlm=np.log(1.0e0-x)
    c1=64.0e0*x*(1.0e0-x)*dlm-128.0e0*x*dlx-32.0e0-160.0e0*x +544.0e0*x*x/3.0e0+32.0e0/x/3.0e0
    res = tr * ca * c1
    return res

@nb.njit("f8(f8)", cache=True)
def clg2am0_aq(x):
    dlx=np.log(x)
    dlm=np.log(1.0e0-x)
    a1=64.0e0*x*(1.0e0-x)*dlm-128.0e0*x*dlx-32.0e0-160.0e0*x +544.0e0*x*x/3.0e0+32.0e0/x/3.0e0
    b1=32.0e0*x*dlx+16.0e0*(1.0e0-2.0e0*x*x+x)
    res = tr * ( ca * a1 + cf * b1 )
    return res

@nb.njit("f8(f8)", cache=True)
def clg2am0_a0(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    dlm2=dlm*dlm
    dlp=np.log(1.0e0+x)
    s11=wgplg(1,1,1.0e0-x)
    s11m=wgplg(1,1,-x)
    a2=96.0e0*x*dlx2+(64.0e0*x*x-192.0e0*x)*dlx*dlm+(32.0e0 -416.0e0*x*x+256.0e0*x)*dlx+32.0e0*x*(1.0e0-x)*dlm2+( -32.0e0+928.0e0*x*x/3.0e0-288.0e0*x+32.0e0/x/3.0e0)*dlm +64.0e0*x*x*zeta2-128.0e0*x*s11+64.0e0*x*(1.0e0+x)*(s11m +dlx*dlp)+32.0e0/3.0e0-1696*x*x/9.0e0+544.0e0*x/3.0e0 -32.0e0/x/9.0e0
    b2=-(64.0e0*x*x*x/5.0e0+64.0e0*x/3.0e0)*dlx2+32.0e0*x *(s11+dlx*dlm)+(-208.0e0/15.0e0+192.0e0*x*x/5.0e0 -416.0e0*x/5.0e0-64.0e0/x/15.0e0)*dlx+(16.0e0-64.0e0*x*x +48.0e0*x)*dlm+(128.0e0*x*x*x/5.0e0-64.0e0*x/3.0e0)*zeta2 +(128.0e0*x*x*x/5.0e0-64.0e0*x/3.0e0+64.0e0/x/x/15.0e0) *(s11m+dlx*dlp)-256.0e0/15.0e0+672.0e0*x*x/5.0e0-608.0e0 *x/5.0e0+64.0e0/x/15.0e0
    res = tr * ( ca * a2 + cf * b2 )
    return res

@nb.njit("f8(f8)", cache=True)
def c2g2am0_aqf(x):
    dlx=np.log(x)
    dlm=np.log(1.0e0-x)
    c1=-248.0e0*x*x/3.0e0+64.0e0*x+8.0e0+32.0e0/x/3.0e0 +(32.0e0*x*x-32.0e0*x+16.0e0)*dlm+(64.0e0*x+16.0e0)*dlx
    res = tr * ca * c1
    return res

@nb.njit("f8(f8)", cache=True)
def c2g2am0_af(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    dlm2=dlm*dlm
    s11=wgplg(1,1,1.0e0-x)
    c2=(-16.0e0+32.0e0*x-32.0e0*x*x)*zeta2+1124.0e0*x*x/3.0e0 -968.0e0*x/3.0e0-172.0e0/3.0e0+16.0e0/x/3.0e0+(16.0e0 -32.0e0*x+32.0e0*x*x)*dlm2-(8.0e0+32.0e0*x)*dlx2+(248.0e0 *x*x/3.0e0-256.0e0*x-8.0e0)*dlx+(32.0e0/x/3.0e0-8.0e0 +192.0e0*x-632.0e0*x*x/3.0e0)*dlm+(96.0e0*x-32.0e0*x*x) *dlx*dlm+(64.0e0*x+16.0e0)*s11
    res  = tr * ca * c2
    return res

@nb.njit("f8(f8)", cache=True)
def c2g2am0_aq2(x):
    dlx=np.log(x)
    dlm=np.log(1.0e0-x)
    a1=16.0e0/x/3.0e0-124.0e0*x*x/3.0e0+32.0e0*x+4.0e0 +(16.0e0*x*x-16.0e0*x+8.0e0)*dlm+(32.0e0*x+8.0e0)*dlx
    b1=-2.0e0+8.0e0*x+(16.0e0*x*x-16.0e0*x+8.0e0)*dlm +(-16.0e0*x*x+8.0e0*x-4.0e0)*dlx
    res = tr * ( ca * a1 + cf * b1 )
    return res

@nb.njit("f8(f8)", cache=True)
def c2g2am0_aq(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    dlm2=dlm*dlm
    dlp=np.log(1.0e0+x)
    s111mx=wgplg(1,1,1.0e0-x)
    s11mx=wgplg(1,1,-x)
    a2=-(16.0e0+32.0e0*x*x)*zeta2+1628.0e0*x*x/9.0e0 -368.0e0*x/3.0e0-220.0e0/3.0e0+208.0e0/x/9.0e0 +(16.0e0*x*x-16.0e0*x+8.0e0)*dlm2-(48.0e0*x+16.0e0) *dlx2+(-536.0e0*x*x/3.0e0+160.0e0*x-8.0e0+32.0e0/x/3.0e0) *dlm+(200.0e0*x*x-192.0e0*x)*dlx+(96.0e0*x-32.0e0*x*x) *dlx*dlm+(64.0e0*x+16.0e0)*s111mx-(32.0e0*x*x+32.0e0*x+16.0e0) *(s11mx+dlx*dlp)
    b2=(-64.0e0*x*x+64.0e0*x-32.0e0)*zeta2+16.0e0*x*x-68.0e0*x +36.0e0+(32.0e0*x*x-32.0e0*x+16.0e0)*dlm2+(32.0e0*x*x -16.0e0*x+8.0e0)*dlx2+(-80.0e0*x*x+96.0e0*x-28.0e0)*dlm +(80.0e0*x*x-48.0e0*x+8.0e0)*dlx+(-64.0e0*x*x+48.0e0*x -24.0e0)*dlx*dlm+(8.0e0-16.0e0*x)*s111mx
    res  = tr * ( ca * a2 + cf * b2 )
    return res

@nb.njit("f8(f8)", cache=True)
def c2g2am0_a0(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlx3=dlx2*dlx
    dlm=np.log(1.0e0-x)
    dlm2=dlm*dlm
    dlm3=dlm2*dlm
    dlp=np.log(1.0e0+x)
    dlp2=dlp*dlp
    s11=wgplg(1,1,1.0e0-x)
    s121mx=wgplg(1,2,1.0e0-x)
    s12mx=wgplg(1,2,-x)
    s211mx=wgplg(2,1,1.0e0-x)
    s21mx=wgplg(2,1,-x)
    s111mx=wgplg(1,1,1.0e0-x)
    s11mx=wgplg(1,1,-x)
    z=(1.0e0-x)/(1.0e0+x)
    s21z=wgplg(2,1,z)
    s21mz=wgplg(2,1,-z)
    a31=dlx3*(16.0e0/3.0e0+16.0e0*x)+ dlx2*dlm*(-8.0e0+16.0e0*x*x-64.0e0*x)+ dlx2*dlp*(12.0e0+32.0e0*x*x+24.0e0*x)+ dlx2*(-114.0e0*x*x+184.0e0*x)+ dlx*dlm2*(-16.0e0*x*x+48.0e0*x)+ dlx*dlm*dlp*(-16.0e0-32.0e0*x*x-32.0e0*x)+ dlx*dlm*(16.0e0+292.0e0*x*x-288.0e0*x)+ dlx*dlp2*(8.0e0+16.0e0*x)
    a32=dlx*dlp*(-48.0e0+208.0e0*x*x/3.0e0+16.0e0*x- 32.0e0/x/3.0e0)+ dlx*zeta2*(-16.0e0+32.0e0*x*x-160.0e0*x)+ dlx*s111mx*(+32.0e0*x)+ dlx*s11mx*(24.0e0+32.0e0*x*x+48.0e0*x)+ dlx*(292.0e0/3.0e0-5780.0e0*x*x/9.0e0+332.0e0*x)+ dlm2*(-6.0e0-214.0e0*x*x/3.0e0+64.0e0*x+16.0e0/x/3.0e0)+ zeta2*dlm*(-40.0e0-64.0e0*x*x+48.0e0*x)
    a33=dlm*s111mx*(16.0e0+64.0e0*x)+ dlm*s11mx*(-16.0e0-32.0e0*x*x-32.0e0*x)+ dlm*(-112.0e0/3.0e0+2996.0e0*x*x/9.0e0-860.0e0*x/3.0e0 +208.0e0/x/9.0e0)+ zeta2*dlp*(8.0e0+16.0e0*x)+ dlp*s11mx*(16.0e0+32.0e0*x)+ s21mz*(-16.0e0-32.0e0*x*x-32.0e0*x)+ s21z*(16.0e0+32.0e0*x*x+32.0e0*x)
    a34=zeta2*(-4.0e0+796.0e0*x*x/3.0e0-208.0e0*x-32.0e0/x)+ zeta3*(-12.0e0-8.0e0*x*x-56.0e0*x)+ s111mx*(20.0e0+80.0e0*x*x/3.0e0-64.0e0*x+64.0e0/x/3.0e0)+ s211mx*(-16.0e0-128.0e0*x)+ s121mx*(40.0e0+144.0e0*x)+ s11mx*(-48.0e0+208.0e0*x*x/3.0e0+16.0e0*x-32.0e0/x/3.0e0)+ s21mx*(-24.0e0-48.0e0*x)+ s12mx*(16.0e0+32.0e0*x)+80.0e0/x/9.0e0+ 466.0e0/9.0e0-878.0e0*x*x/9.0e0+260.0e0*x/9.0e0
    a3=a31+a32+a33+a34
    b31=dlx3*(-8.0e0/3.0e0-32.0e0*x*x/3.0e0+16.0e0*x/3.0e0)+ dlx2*dlm*(16.0e0+48.0e0*x*x-32.0e0*x)+ dlx2*dlp*(16.0e0+16.0e0*x*x+32.0e0*x)+ dlx2*(-4.0e0-96.0e0*x*x*x/5.0e0-52.0e0*x*x+8.0e0*x/3.0e0)+ dlx*dlm2*(-20.0e0-48.0e0*x*x+40.0e0*x)+ dlx*dlm*(24.0e0+168.0e0*x*x-160.0e0*x)+ dlx*dlp2*(-32.0e0-32.0e0*x*x-64.0e0*x)+ dlx*dlp*(96.0e0+192.0e0*x*x*x/5.0e0+128.0e0*x/3.0e0)
    b32=16.0e0*dlx*dlp/x/x/15.0e0-16.0e0*dlx/x/15.0e0+ dlx*zeta2*(32.0e0+64.0e0*x*x-64.0e0*x)+ dlx*s111mx*(32.0e0*x*x)+ dlx*s11mx*(-32.0e0-32.0e0*x*x+64.0e0*x)+ dlx*(-712.0e0/15.0e0-672.0e0*x*x/5.0e0+136.0e0*x/5.0e0)+ dlm3*(8.0e0+16.0e0*x*x-16.0e0*x)+ dlm2*(-22.0e0-84.0e0*x*x+88.0e0*x)+ zeta2*dlm*(-32.0e0*x*x)
    b33=dlm*s111mx*(8.0e0-16.0e0*x)+ dlm*(28.0e0+96.0e0*x*x-132.0e0*x)+ zeta2*dlp*(-32.0e0-32.0e0*x*x-64.0e0*x)+ dlp*s11mx*(-64.0e0-64.0e0*x*x-128.0e0*x)+ zeta2*(48.0e0+192.0e0*x*x*x/5.0e0+104.0e0*x*x- 208.0e0*x/3.0e0)+ zeta3*(112.0e0+192.0e0*x*x-96.0e0*x)
    b34=s111mx*(-24.0e0+64.0e0*x*x-48.0e0*x)+ s211mx*(-24.0e0-32.0e0*x*x+48.0e0*x)+ s121mx*(-32.0e0+64.0e0*x)+ s11mx*(96.0e0+192.0e0*x*x*x/5.0e0+128.0e0*x/3.0e0)+ 16.0e0*s11mx/x/x/15.0e0+16.0e0/x/15.0e0+ s21mx*(96.0e0+96.0e0*x*x-64.0e0*x)+ s12mx*(-64.0e0-64.0e0*x*x-128.0e0*x)- 904.0e0/15.0e0+328.0e0*x*x/5.0e0+68.0e0*x/5.0e0
    b3=b31+b32+b33+b34
    res  = tr * ( ca * a3 + cf * b3 )
    return res

@nb.njit("f8(f8)", cache=True)
def clps2am0_af(x):
    dlx=np.log(x)
    c1=32.0e0/3.0e0/x+64.0e0*x*x/3.0e0 -32.0e0-32.0e0*x*dlx
    res = cf * tr * c1
    return res

@nb.njit("f8(f8)", cache=True)
def clps2am0_aq(x):
    dlx=np.log(x)
    a1=-32.0e0*x*dlx-32.0e0+64.0e0*x*x/3.0e0+32.0e0/x/3.0e0
    res = cf * tr * a1
    return res

@nb.njit("f8(f8)", cache=True)
def clps2am0_a0(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    spx=wgplg(1,1,1.0e0-x)
    a2=32.0e0*x*(dlx2-dlx*dlm-spx)+(-32.0e0+64.0e0*x*x/3.0e0 +32.0e0/x/3.0e0)*dlm+(32.0e0-64.0e0*x*x-32.0e0*x)*dlx +32.0e0/3.0e0+320.0e0*x*x/9.0e0-128.0e0*x/3.0e0 -32.0e0/x/9.0e0
    res = cf * tr * a2
    return res

@nb.njit("f8(f8)", cache=True)
def c2ps2am0_aqf(x):
    dlx=np.log(x)
    c1=-32.0e0*x*x/3.0e0-8.0e0*x+8.0e0+32.0e0/x/3.0e0 +16.0e0*(1.0e0+x)*dlx
    res = cf * tr * c1
    return res

@nb.njit("f8(f8)", cache=True)
def c2ps2am0_af(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    spx=wgplg(1,1,1.0e0-x)
    c2=128.0e0*x*x/3.0e0+16.0e0*x/3.0e0-160.0e0/3.0e0 +16.0e0/x/3.0e0+8.0e0*(1.0e0+x)*(-dlx2+2.0e0*dlx*dlm +2.0e0*spx)+(-32.0e0*x*x/3.0e0-8.0e0*x+8.0e0+32.0e0/x/3.0e0) *dlm+(32.0e0*x*x/3.0e0-40.0e0*x-8.0e0)*dlx
    res  = cf * tr * c2
    return res

@nb.njit("f8(f8)", cache=True)
def c2ps2am0_aq2(x):
    dlx=np.log(x)
    a1=-16.0e0*x*x/3.0e0-4.0e0*x+4.0e0+16.0e0/x/3.0e0 +8.0e0*(1.0e0+x)*dlx
    res = cf * tr * a1
    return res

@nb.njit("f8(f8)", cache=True)
def c2ps2am0_aq(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    s11=wgplg(1,1,1.0e0-x)
    a2=-64.0e0*x*x/9.0e0+160.0e0*x/3.0e0-208.0e0/3.0e0 +208.0e0/x/9.0e0+32.0e0*x*x*dlx+16.0e0*(1.0e0+x)*(-dlx2+dlx*dlm +s11)+(-32.0e0*x*x/3.0e0-8.0e0*x+8.0e0+32.0e0/x/3.0e0) *dlm
    res  = cf * tr * a2
    return res

@nb.njit("f8(f8)", cache=True)
def c2ps2am0_a0(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlx3=dlx*dlx2
    dlm=np.log(1.0e0-x)
    dlm2=dlm*dlm
    dlp=np.log(1.0e0+x)
    s11=wgplg(1,1,1.0e0-x)
    s12=wgplg(1,2,1.0e0-x)
    s21=wgplg(2,1,1.0e0-x)
    s11m=wgplg(1,1,-x)
    a3=(1.0e0+x)*(16.0e0*dlx3/3.0e0-16.0e0*dlx2*dlm+8.0e0 *dlx*dlm2-32.0e0*zeta2*dlx+16.0e0*dlm*s11+32.0e0*s12 -16.0e0*s21)+(40.0e0*x-16.0e0*x*x)*dlx2+32.0e0*x*x*dlx *dlm+(280.0e0/3.0e0-704.0e0*x*x/9.0e0-88.0e0*x)*dlx +(4.0e0-16.0e0*x*x/3.0e0-4.0e0*x+16.0e0/x/3.0e0)*dlm2 +(-208.0e0/3.0e0-64.0e0*x*x/9.0e0+160.0e0*x/3.0e0 +208.0e0/x/9.0e0)*dlm+(-16.0e0+64.0e0*x*x/3.0e0-16.0e0*x -32.0e0/x)*zeta2+(16.0e0-16.0e0*x+64.0e0/x/3.0e0 +32.0e0*x*x/3.0e0)*s11+(-32.0e0-32.0e0*x*x/3.0e0-32.0e0 *x-32.0e0/x/3.0e0)*(s11m+dlx*dlp)+304.0e0/9.0e0+832.0e0 *x*x/9.0e0-1216.0e0*x/9.0e0+80.0e0/x/9.0e0
    res  = cf * tr * a3
    return res

@nb.njit("f8(f8)", cache=True)
def clns2am0_aq(x):
    res = 16e0 * cf * tr * x / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def clns2am0_a0(x):
    res = 16e0 * cf * tr * ( x * np.log( 1e0 - x ) - 2e0 * x * np.log(x) - 25e0 * x / 6e0 + 1e0 ) / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2am0_aq2(x):
    b1=(-1e0-x)*2.0e0
    res = 2e0 * cf * tr * b1 / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2am0_aq(x):
    dlx=np.log(x)
    dlm=np.log(1.0e0-x)
    a1=((-8.0e0*(1.0e0+x*x)*dlx/(1.0e0-x)+13.0e0*x+1.0e0) + (-1e0-x)*(4.0e0*dlm-29.0e0/3.0e0))
    res = 2e0 * cf * tr * a1 / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2am0_a0(x):
    dlx=np.log(x)
    dlx2=dlx*dlx
    dlm=np.log(1.0e0-x)
    dlm2=dlm*dlm
    spx=wgplg(1,1,1.0e0-x)
    a2=(1.0e0+13.0e0*x)*dlm-(3.0e0+23.0e0*x)*dlx+29.0e0/6.0e0 -295.0e0*x/6.0e0+(1.0e0+x*x)*(-4.0e0*spx-8.0e0*dlx *dlm+6.0e0*dlx2+67.0e0*dlx/3.0e0)/(1.0e0-x)
    b2=(-1e0-x)*(-4.0e0*zeta2+2.0e0*dlm2 -29.0e0*dlm/3.0e0+359e0/18.0e0)
    res = 2e0 * cf * tr * ( a2 + b2 ) / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2bm0_aq2(x):
    z = 2e0 / ( 1e0 - x )
    res = z * 4e0 * cf * tr / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2bm0_aq(x):
    dlm = np.log( 1e0 - x )
    z   = 2e0 / ( 1e0 - x )
    res = z * 2e0 * cf * tr * ( 4e0 * dlm - 29e0 / 3e0 ) / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2bm0_a0(x):
    dlm  = np.log( 1e0 - x )
    dlm2 = dlm * dlm
    z    = 2e0 / ( 1e0 - x )
    res = z * 2e0 * cf * tr * ( - 4e0 * zeta2 + 2e0 * dlm2 - 29e0 * dlm / 3e0 + 359e0 / 18e0 ) / 3e0
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2cm0_aq2(x):
    dlm = np.log( 1e0 - x )
    res = 8e0 * cf * tr * dlm / 3e0 + 2e0 * cf * tr
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2cm0_aq(x):
    dlm  = np.log( 1e0 - x )
    dlm2 = dlm * dlm
    res = 4e0 * cf * tr * ( 2e0 * dlm2 - 29e0 * dlm / 3e0 ) / 3e0 - cf * tr * ( 32e0 * zeta2 / 3e0 + 38e0 / 3e0 )
    return res

@nb.njit("f8(f8)", cache=True)
def c2ns2cm0_a0(x):
    dlm  = np.log( 1e0 - x )
    dlm2 = dlm * dlm
    dlm3 = dlm2 * dlm
    res = 4e0 * cf * tr * ( - 4e0 * zeta2 * dlm + 2e0 * dlm3 / 3e0 - 29e0 * dlm2 / 6e0 + 359e0 * dlm / 18e0 ) / 3e0 + cf * tr * ( 268e0 * zeta2 / 9e0 + 265e0 / 9e0 )
    return res
