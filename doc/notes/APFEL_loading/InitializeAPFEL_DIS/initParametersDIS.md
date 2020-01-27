# initParametersDIS

If not already set initialize parameters to default.


Then check the consistency of some inputs:
- MassScheme: one of the allowed
- ProcessDIS: one of the allowed
- PolarizationDIS: | p | <= 1
- ProjectileDIS: one of the allowed
- TargetDIS: one of the allowed
- SelectCharge: one of the allowed
- ScVarProc: 0 <= s <= 1

each of the preceding should hold, otherwise a warning would be printed and it will exit(-10).

Then:
- SetRenFacRatio: krenQ != 1 or kfacQ != 1
    - SetRenFacRatio(dsqrt(krenQ/kfacQ))
    - if ScVarProc = 1
        - SetRenFacRatio(1d0)
- if TimeLike set to True:
    - MassScheme: = 'ZM-VNFS' (and set it)
    - TMC: not available (and switch it off)
    - ProjectileDIS: = 'electron' (and set it)
    - PolarizationDIS: = 0 (and set it)
    - TargetDIS: = 'proton' (and set it)
        - warning silenced for some reasons
    - ProcessDIS: != 'CC' (and set 'EM')
        - warning silenced for some reasons
- if Polarized set to True:
    - MassScheme: = 'ZM-VNFS' (and set it)
    - TMC: not available (and switch it off)
    - ipt: < 2 (and set it to 1)
        - also if not set it sets ipt to 1
- if MassScheme = 'FFNS' or 'FFN0':
    - warning
    - if MassScheme\[5\] = x in \[3,4,5,6\]:
        - warning
        - call SetFFNS(x)
    - else
        - warning
        - call SetFFNS(x)
- else (MassScheme != 'FFNS' or 'FFN0')
    - if 6 < Nf_FF < 3: Nf_FF = 3
        - warning: is VNFS
        - set VNFS
- if MassScheme = 'FONLL-A':
    - warning
    - set pto = 1
- if MassScheme = 'FONLL-B':
    - warning
    - set pto = 1
- if MassScheme = 'FONLL-C':
    - warning
    - set pto = 2
- if DeltaR = 1:
    - warning
    - set it to 0
- if DynScVar:
    - warning
    - SetRenQRatio(1d0)
    - SetFacQRatio(1d0)
- if IntrinsicCharm:
    - if Nf_FF > 3:
        - warning
        - set Nf_FF to 3
