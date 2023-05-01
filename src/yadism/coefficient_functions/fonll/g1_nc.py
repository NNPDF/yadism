import numba as nb
import numpy as np
from ..partonic_channel import RSL
from . import partonic_channel as pc
from ..special.zeta import zeta2, zeta3
from ..special.nielsen import nielsen
from eko.constants import CA as ca
from eko.constants import CF as cf
from eko.constants import TR as tr

# complex :math:`S_{n,m}(x)`-> nielsen(N, M, X)

@nb.njit("f8(f8,f8[:])", cache=True)
class NonSinglet():
    def NNLO(z, args):
        """Massive asymptotic polarized flavor non–singlet Wilson coefficient with in the MSbar scheme. 

        |ref| implements :eqref:`254`, :cite:`Blümlein` (needs to be added).
        """
        L = args[0]
        dlz=np.log(z) #H(0;x)
        dlz2 =dlz*dlz  #H(0;x)^2
        dlm = (-1)* np.log(1.0e0-z) #H(1;x) (relative to the definitions in other scripts, theres an extra (-1), im defining it according to 'Harmonic Polylogarithms' E. Remiddia,b and J. A. M. Vermaseren )
        dlm2 =dlm*dlm
        dlp=np.log(1.0e0+z) #H(-1;x)

        res= cf*tr*((-4/3)* np.power(L,2)*(1+ z) + (4/27)* (-47-218*z+36* zeta2 +36*z*zeta2)+ ((265/9)+((2*L)/3) + 2*np.power(L,2))*(np.delta(1-z)) - 4*(1 + z)*dlz2 +L *((-8/9)*(-1 + 11*z) - (8/3)*(1 + z) *dlz) - (8/9)*(5 + 14*z) * dlm - (4/3)* (1 + z)* dlm2+(-(8/9)*(13 + 28*z)-(8/3)*(1 + z)*dlm) - (8/3)*(1 + z)* nielsen(0,1,z) + 1/(1-z)*((8*np.power(L,2))/3 - (2/27)*(-359 + 144*zeta2) + 8*dlz + L*((80/9)+(16/3)*dlz) + (116/9)*dlm + (8/3)*dlm2 + dlz*((268/9) + (16/3)*dlm) + (16/3)* nielsen(0,1,z))) 
        #remove delta later
        return res