# InitializeAPFEL

**WARNING:**
this part belongs to Evolution, so is mainly supposed to be managed by `eko` rather
than `yadism`

## Read input parameters: *initParameters*
see [initParameters](./initParameters.md)

## Report DIS parameters: *ReportParameters*
- WelcomeMessage
- print parameters values (with description)

## Initialize alphas grid: *initGridAlpha*

## For igrid
- for igrid in range(ngrid):
  - **Initialize x-space grid:** initGrid
  - **Flavour Number Scheme**:
    - if Evs = FFNS:
      - set nfi & ff to Nf_FF
    - elif Evs = VFNS:
      - Q2max > m2th(x), x in \[4,5,6]
        - set nff to x
      - else
        - set nff to 3
      - Q2min > m2th(x), x in \[4,5,6]
        - set nfi to x
      - else
        - set nfi to 3
      - if nfi < nff
        - for y in (nfi+1, nff): initIntegralsMatching(y)
      - elif nfi > nff
        - for y in (nfi, nff+1): initIntegralsMatching(y)
  - **Evaluate evolution operators on the grid:**
    - if QCD:
      - for y in (nfi, nff):
        - initIntegralsQCD(y)
      - if Smallx: initIntegralsQCDRes
    - elif QUniD:
      - for y in (nfi, nff):
        - initIntegralsQCD(y)
        - for z in (2, 3): initIntegralsQED(y, z)
      - if Smallx: initIntegralsQCDRes
- end for

## Initialization time
- **if Welcome:** print time spent to initialize
