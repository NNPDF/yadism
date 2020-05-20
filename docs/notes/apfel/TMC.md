# TMC
How APFEL computes target mass corrections

## Variable definition
Source: `F2light.f` and similar

As in the docs pdf (`dis.pdf`)  aux variables are defined (`xi`, `rho` that is
called `rhop` in the code) directly in `F2light.f`

## Integration
Source: `ConvolutePDFwithDISOperators.f` for `I2`
Source: `ComputeDISOperators.f` for `OpI2`

The integration is already provided, since it is precomputed on a grid. The
matrix of coefficients it's called `I2(ihq,g,alpha)` where:
- `ihq` is the flavour number (so 3 for light, 4 for charm and so on)
- `g` is the subgrid number (since APFEL is breaking the global grid currently
    we don't know why), 0 means the joint (total) grid
- `alpha` is the replacement for `xi` value, i.e. it is its discretization over
    the grid

Two kinds of `I2` are provided:
- `I2` as described above, used when pdf are already applied
- `OpI2`, that is the correspondent of `OpF2`, in which instead of a number it
    provides an array to be dotted with the pdf once available (so it has one
    index more w.r.t. the former, since it is waiting for the pdf array)

Since `OpI2` has one interpolation index more it has also another index on a
subgrid (in order to identify the interpolation two index are used, one to get
the subgrid and the other internal to the subgrid), so the signature it is
`OpI2(jgrid,ihq,ipdf,alpha,beta)`:
- `jgrid` and `alpha` are the subgrid and internal index for `xi` interpolant
- `ipdf` and `beta` are the subgrid and internal index for pdf interpolant
- `ihq` flavour index, as before

### Integration
Source: `RSLintegralsDIS.f` for `J_TMC`
Source: `Evolution/interpolants.f` for `w_int`

The actual integral of `I2` it's performed not on `F2(x)/x^2`, but on the basis
functions (as documented in `dis.pdf` eq. 2.5), and the result of integration of
basis functions is provided as another matrix `J_TMC(igrid,beta,alpha)`:
- `igrid` and `alpha` are the subgrid and internal index for `xi` interpolant
- `beta` is the index on which the sum is performed (the discrete replacement of
    `F2` integration)

`J_TMC` it's defined integrating (it uses `dgauss`) the `w_int(k,beta,x)`
polynomials:
- `k` is the interpolation degree
- `beta` is the interpolant index
- `x` is the argument of the polynomial function

For integrating `J_TMC` polynomials of degree 1 are used.

#### About integration routine
Note that `J_TMC` is computed through `dgauss` function of `cernlib` (see
http://hep.fi.infn.it/cernlib.pdf pp.94-95), which signature is
`dgauss(integrand,a,b,eps)`
- `integrand` is the integrand
- `a` and `b` are extremes of integration
- `eps` is the required precision (relative is the integration `|I|>1`, otherwise
    absolute)
Since the integrand in APFEL are interpolants of degree 1 they are always
smaller than 1, and with a domain smaller than `[0,1]`, so we have for sure
`|I|<1`. Since APFEL is also requiring an `eps = 1e-5` the *absolute*
integration error of APFEL it's probably of that order of magnitude.
