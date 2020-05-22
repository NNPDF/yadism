Interpolation
=============

Interpolation kicks in the game in a lot of ways, namely 3:

- there is an interpolation involved at the **pdf level**, that is really the only
  one `yadism` cares about, and is managed through `eko`: pdfs are delivered as
  an array of coefficient over an interpolation basis made of polynomials (of
  `x` or `logx`, chosen as an option)
- there is an interpolation involved at the **structure functions level**: this
  is done by `APFEL` since it's precomputing the structure functions on the
  xgrid at initialization time, and when asked for a specific observable it
  interpolates it on the precomputed grid
  this is not done in `yadism` since we are computing the structure functions
  only when required, so we are computing exactly on that point and there is no
  need to interpolate it
  *note*: we can also do this quite easily, if required or for benchmarking,
  since the caching system makes it easier to switch on *precomputing model*,
  because if we setup the interpolation the precomputed grid is already stored,
  even if as a cache
  *note2*: everything in `APFEL` is discretized, so not only the structure
  functions themselves, but also everything that is integrated or the result of
  an integral (such as `I2` in `TMC`, see 2.5 in dis pdf in `apfel` docs, there
  is already a basis function involved to discretized the integrand, but also
  the result will be discretized on `xi` inserting other basis functions, as it
  is done in `F2light.f` for example)
- there is a second *really bad* interpolation involved at the *level of the
  pdf* (at least in benchmarking), that is the `lhapdf` one: in order to get
  the pdf to interpolate we are using `lhapdf` grids. So `eko`, e.g., it's
  making pdf interpolation over our `xgrid`, but when evaluating the `pdf` on
  our `xgrid` you should take care that this is already interpolated, since our
  `xgrid` may not match the `lhapdf` one.
  This is done in both `yadism` and `APFEL`, so it's not a source of
  discrepancy, but it's make it approximate w.r.t. to the exact shape (for
  example when we are generating the `lhapdf` grids with a known function)
  *note*: this is not happening in `toyLH`, since we are not passing through
  `lhapdf` in that case, but mimic it
