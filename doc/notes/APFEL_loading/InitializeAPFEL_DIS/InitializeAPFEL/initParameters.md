# initParameters

If not already set initialize parameters to default.

Then check the consistency of some inputs:
- Th: 'QCD' or 'QUniD' allowed
- Evs: 'FF' or 'VF' allowed
  - if Evs = 'FF': 3 <= Nf_FF <= 6
- ipt: 0 <= ipt <= 2
- mass_scheme: 'Pole' or 'MSbar' allowed
- AlphaEvol: 'exact', 'expanded' or 'lambda' allowed
  - if AlphaEvol = 'lambda':  Th 'QUniD' not allowed
- PDFEvol: 'exactmu', 'exactalpha', 'expandalpha' or 'truncated' allowed
- if Smallx
  - TimeLike not allowed
  - Polarized not allowed
  - kren != 1 not allowed
  - LogAcc = 0, 1
- m2ph
  - two heavy quarks' masses equal not allowed
  - they should be ordered
  - k2th: also the thresholds should be ordered
- if mass_scheme = 'MSbar':
  - each heavy quark mass should be define at a scale higher than the mass itself
- nq2LHA <= nq2max & nxLHA <= nxmax
  - i.e. LHA grids' points should not exceed the maximum allowed (both for x and Q2)
- if Polarized
  - TimeLike not allowed
  - if 'VFNS': ipt < 2 (NNLO not allowed)

each of the preceding should hold, otherwise a warning would be printed and it will exit(-10).

Instead the following have a default to switch if incompatible inputs are detected:
- EvolOp
  - & FastEvol not allowed together
    - disable FastEvol
  - & !ExtGrids => LockGrids
    - enable LockGrids
  - & Th = 'QUniD'
    - set TauMass to 0 (∞ yields same behavior)
- ExtGrids => !LockGrids
  - disable LockGrids
- Polarized & ipt > 1
  - warning only: polarized at NNLO is incomplete
- NLOQED & Th!='QUniD'
  - disable NLOQEDCorrections

each one will emit a warning the same if something incompatible is found.

- ComputeHeavyQuarkThresholds
- if mass_scheme = MSbar
  - ComputeRGInvariantMasses
- if AlphaEvol = 'lambda'
  - LambdaQCDnf: compute values of LambdaQCD for all the number of flavours
- ThresholdAlphaQCD
- is Smallx
  - initHELL
