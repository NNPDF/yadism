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
# for the light coefficient function; singlet, non singlet, gluonic 
#LS= LNS + LPS
# for the heavy coefficient function; singlet (only pure singlet contributes), gluonic 
# HS= HPS

@nb.njit("f8(f8,f8[:])", cache=True)
class NonSinglet():
    def NNLO(z, args):
        """Massive asymptotic polarized flavor non–singlet Wilson coefficient in the MSbar scheme. 

        |ref| implements :eqref:`254`, :cite:`Blümlein` (needs to be added). (coupling to the light quark)
        """
        L = args[0]
        dlz=np.log(z) #H(0;x)
        dlz2 =dlz*dlz  #H(0;x)^2
        dlm = (-1)* np.log(1.0e0-z) #H(1;x) (relative to the definitions in other scripts, theres an extra (-1), im defining it according to 'Harmonic Polylogarithms' E. Remiddia,b and J. A. M. Vermaseren )
        dlm2 =dlm*dlm

        res= cf*tr*((-4/3)* np.power(L,2)*(1+ z) + (4/27)* (-47-218*z+36* zeta2 +36*z*zeta2)+ ((265/9)+((2*L)/3) + 2*np.power(L,2))*(np.delta(1-z)) - 4*(1 + z)*dlz2 +L *((-8/9)*(-1 + 11*z) - (8/3)*(1 + z) *dlz) - (8/9)*(5 + 14*z) * dlm - (4/3)* (1 + z)* dlm2+(-(8/9)*(13 + 28*z)-(8/3)*(1 + z)*dlm) - (8/3)*(1 + z)* nielsen(0,1,z) + 1/(1-z)*((8*np.power(L,2))/3 - (2/27)*(-359 + 144*zeta2) + 8*dlz + L*((80/9)+(16/3)*dlz) + (116/9)*dlm + (8/3)*dlm2 + dlz*((268/9) + (16/3)*dlm) + (16/3)* nielsen(0,1,z))) 
        #remove delta later
        return res
    

    class PureSinglet():
        def NNLO(z, args):
            """Massive asymptotic polarized pure singlet Wilson coefficient with in the Larin scheme. 

            |ref| implements :eqref:`261`, :cite:`Blümlein` (needs to be added). (coupling to the heavy quark)
            """
            L = args[0]
            dlz=np.log(z) #H(0;x)

            dlm = (-1)* np.log(1.0e0-z) #H(1;x) (relative to the definitions in other scripts, theres an extra (-1), im defining it according to 'Harmonic Polylogarithms' E. Remiddia,b and J. A. M. Vermaseren )
            dlp=np.log(1.0e0+z) #H(-1;x)
            nH001z= None#reexpress in terms of lower weight harmonic polylogarithm
            nH011z= None #reexpress in terms of lower weight harmonic polylogarithm

            res= cf*tr*(-(592/3)*(-1 + z)-(32/3)*(9 - 3*z + np.power(z,2))*zeta2 + 16*(1 + z)* zeta3 + (-1*(256/3)*(-2 + z) - 32*(1 + z)*zeta2)* dlz - (32*np.power(1+z,3)*dlp*dlz)/(3*z) + (8/3)*(21+2*np.power(z,2))*np.power(dlz,2)+(16/3)*(1+ z)*np.power(dlz,3) + np.power(L,2)*(20*(-1 + z)-8*(1 + z)*dlz) + L*((-8)*(-1 + z)+8*(-1+3*z)*dlz- 8*(1 + z)*np.power(dlz,2))+(-88*(-1+z)-80*(-1+z)*dlz)*dlm-20*(-1+z)*np.power(dlm,2)+(32*np.power(1+z,3)*nielsen(0,-1,z))/(3*z)+(16*(-1+3*z)+ 32*(1+z)*dlz)*nielsen(0,1,z)-32*(1 + z)*nH001z+16*(1 + z)*nH011z) 
            return res

    class Gluonic_light():
        def NNLO(z, args):
            """Massive asymptotic polarized gluonic Wilson coefficient. 

            |ref| implements :eqref:`277`, :cite:`Blümlein` (needs to be added). (coupling to the light quark)
            """
            L = args[0]
            dlz=np.log(z) #H(0;x)
            dlm = (-1)* np.log(1.0e0-z) #H(1;x) (relative to the definitions in other scripts, theres an extra (-1), im defining it according to 'Harmonic Polylogarithms' E. Remiddia,b and J. A. M. Vermaseren )
            res= (16/3)*np.power(tr,2)*(4*z -3+(2*z-1)*(dlz+dlm))*L
            return res

    class Gluonic_heavy():
        def NNLO(z, args):
            """Massive asymptotic polarized gluonic Wilson coefficient. 

            |ref| implements :eqref:`273`, :cite:`Blümlein` (needs to be added). (coupling to the heavy quark)
            """
            L = args[0]
            dlz=np.log(z) #H(0;x)
            dlm = (-1)* np.log(1.0e0-z) #H(1;x) (relative to the definitions in other scripts, theres an extra (-1), im defining it according to 'Harmonic Polylogarithms' E. Remiddia,b and J. A. M. Vermaseren )
            dlp=np.log(1.0e0+z) #H(-1;x)
            nH001z= None#reexpress in terms of lower weight harmonic polylogarithm 
            nH011z=  None#reexpress in terms of lower weight harmonic polylogarithm
            nH0m1m1z= None
            nH00m1z= None
            nH0m11z= None 
            nH01m1z= None

            res= np.power(L,2)*(-(16/3)*np.power(tr,2)*(-1 + 2*z) + cf*tr*(6+(-1+2*z)*(-4*dlz-8*dlm)) + ca* tr*(48*(-1+z)-16*(1 + z)*dlz+8*(-1 + 2*z)*dlm))+L*(np.power(tr,2))*((16/3)*(-3+4*z)+(-1 + 2*z)*((16/3)*dlz+(16/3)*dlm))+ca*tr*(-8*(-12+11*z)-16*zeta2 +8*(1 +8*z)*dlz-32*(-1 + z)*dlm -8*(-1+2*z)*np.power(dlm,2)+(1 + 2*z)*(-16*dlp*dlz-8*np.power(dlz,2)+ 16* nielsen(0,-1,z)))+ cf*tr*(4*(-17+13*z)- 24*(-1+2*z)*zeta2+16*(-3+2*z)*dlz+4*(-17+20*z)*dlm+(-1+2*z)*(8*np.power(dlz,2)+32*dlz*dlm+16*np.power(dlm,2)-8*nielsen(0,1,z))) +ca*tr*(-(8/3)*(-101 + 104*z) -8(-1- 10*z + 4*np.power(z,2))*zeta3+(4/3)*(194-163*z+6*np.power(z,2))*dlz-(16*(2+3*z + 9*np.power(z,2)+11*np.power(z,3))*dlp*dlz)/(3*z)+16*np.power(z,2)*np.power(dlp,2)*dlz+((2/3)*(126-48*z+41*np.power(z,2)) - 4*(-3-6*z+2*np.power(z,2))*dlp)*np.power(dlz,2) + (8/3)*(3 + 4*z)*np.power(dlz,3)+4*(43-53*z+2*np.power(z,2))*dlm-4*(-53+ 56*z + np.power(z,2))*dlz*dlm+4*(3-6*z +2*np.power(z,2))*np.power(dlz,2)*dlm+ 2*(19-24*z+np.power(z,2))*np.power(dlm,2)+ zeta2*(-(4/3)*(114 - 84*z+47*np.power(z,2))+16*(-1-2*z+np.power(z,2))*dlp- 32*(2+z)*dlz -16*np.power(-1+z,2)*dlm)+(((16*(2+3*z+9*np.power(z,2)+11*np.power(z,3)))/(3*z)) -32*np.power(z,2)*dlp + 8*(-3-6*z +2*np.power(z,2))*dlz)*nielsen(0,-1,z)+ 4*(-19 + 28*z + 2*np.power(z,2))*nielsen(0,1,z)-8*(-7-10*z +2*np.power(z,2))*dlz*nielsen(0,1,z)+(-1 + 2*z)*(-16*dlz*np.power(dlm,2)+ 16*dlm*nielsen(0,1,z))+32*np.power(z,2)*nH0m1m1z- 8*(-3-6*z + 2*np.power(z,2))*nH00m1z + 8*(-9 - 10*z + 2*np.power(z,2))*nH001z+(1 + 2*z)*(16*dlp*nielsen(0,1,z) - 16*nH0m11z -16*nH01m1z) + 48*nH011z)+ cf*tr*(-(20/3)*(-20+17*z)+8*(1 + 14*z + 8*np.power(z,2))*zeta3-(8/3)*(-46+53*z+6*np.power(z,2))*dlz+((16*(4+12*np.power(z,2)+13*np.power(z,3))*dlp*dlz)/(3*z)) -32*np.power(1+z,2)*np.power(dlp,2)*dlz+(-(4/3)*(-27 + 6*z +23*np.power(z,2)) +16*np.power(1+z,2)*dlp)*np.power(dlz,2)-4*(-47 + 41*z + 4*np.power(z,2))*dlm + 8*(8-14*z + np.power(z,2))*dlz*dlm -16*np.power(z,2)*np.power(dlz,2)*dlm - 2*(-33+40*z + 2*np.power(z,2))*np.power(dlm,2) + zeta2*((8/3)*(-60+42*z +29*np.power(z,2)) -32*np.power(1+z,2)*dlp+ 32*np.power(z,2)*dlm+(-1+2*z)*(32*dlz+16*dlm))+(-((16*(4 + 12*np.power(z,2) + 13*np.power(z,3)))/(3*z))+64*np.power(1+z,2)*dlp-32*np.power(-1+z,2)*dlz)*nielsen(0,-1,z) - 16*(-6+np.power(z,2))*nielsen(0,1,z) +32*np.power(-1+z,2)*dlz*nielsen(0,1,z)- 64*np.power(1+z,2)*nH0m1m1z + 32*(1-6*z +np.power(z,2))*nH00m1z-32*np.power(-1+z,2)*nH001z+(-1+2*z)*(-(8/3)*np.power(dlz,3) -16*dlz*np.power(dlm,2) -8*np.power(dlm,3) -16*dlm*nielsen(0,1,z)+ 24*nH011z))
            return res