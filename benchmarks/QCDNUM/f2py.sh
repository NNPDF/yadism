#!/bin/bash

# old
#f2py3 -c qcdnum/usr/usrini.f qcdnum/usr/usrparams.f qcdnum/usr/usrevol.f extpdf.pyf zmstf/src/zmstfs.f \
#  only: qcinit setord getord setalf getalf setcbt extpdf zmstfun : \
# `qcdnum-config --cppflags` `qcdnum-config --ldflags` \
# -I./qcdnum/inc/ -I./zmstf/inc/
# f2py3 -m QCDNUM -c extpdf.pyf qcdnum/usr/usrevol.f `qcdnum-config --cppflags` `qcdnum-config --ldflags` -I./qcdnum/inc/ -I./zmstf/inc/


MODE=1
FILES='qcdnum/usr/usrini.f qcdnum/usr/usrparams.f qcdnum/usr/usrevol.f qcdnum/usr/usrgrd.f zmstf/src/zmstfs.f'


#if ["$MODE" -eq "1"] then
#f2py3 --overwrite-signature -m QCDNUM -h QCDNUM.template.pyf $FILES \
#  only: qcinit setord getord setalf getalf setcbt extpdf zmstfun gxmake gqmake : ;
#fi;

#if ["$MODE" -eq "2"] then
f2py3 -m QCDNUM -c QCDNUM.pyf $FILES\
 `qcdnum-config --cppflags` `qcdnum-config --ldflags` -I./qcdnum/inc/ -I./zmstf/inc/ ;
#fi;
