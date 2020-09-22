# Questions
What I don't know about APFEL work __Alessandro

- Theory
  - I don't know the definition and the role of some parameters in the theory
    - FNS
    - TMC
    - IntrinsicCharm
    - ...
- InitializeAPFEL:
  - alpha grid
    - what is it?
  - igrid, ngrid
    - what are they?
    - and why initGrid is called repeatedly without taking any value
      - and also all the other steps are repeated
- InitializeAPFEL_DIS:
  - SIA Integrals
    - and something about integrals of coefficient and interpolation functions in general
  - bunch of initIntegrals functions:
    - initIntegralsMatching (InitializeAPFEL)
    - initIntegralsQCD (InitializeAPFEL)
    - initIntegralsQCDRes (InitializeAPFEL)
    - initIntegralsQED (InitializeAPFEL)
    - initIntegralsSIA (InitializeAPFEL_DIS)
    - initIntegralsDIS (InitializeAPFEL_DIS)
    - initIntegralsDISRes (InitializeAPFEL_DIS)
- initParameters:
  - what are the 'heavy quark thresholds'?
  - 'each heavy quark mass should be define at a scale higher than the mass itself' why?
  - what are the external grids?
  - what are the subgrids?
  - what does it mean that the grids are locked?
  - what is HELL?
- initParametersDIS:
  - what is the ScaleVariationProcedure?
    - in particular what is the ScaleVariation?
  - why krenQ = ratioR^2?
    - same for fac scale
  - what is the Z propagator correction DeltaR?
  - which is the exact definition of DIS polarization?
  - what is the Mass Scheme?
  - what is DampingFONLL?
    - and what is FONLL at all...