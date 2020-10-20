# Coefficient Functions

- numba is able to compile only with local objects
  - e.g.: $ quark_0(x) + \alpha quark_1(x) $
  - numba is able to compile `quark_0` and `quark_1`
  - numba is not able to compile the sum, (that should be defined as a new
      function `def quark(x): return quark_0(x) + alpha * quark_1(x)`) since
      external (non-local) objects are involved, `quark_0` and `quark_1`

- if inlining is required maybe we should think about encoding coefficient
    functions only in C++

- numba is able to deal with global variables, but they are evaluated as soon as
    the function is compiled (called) the first time

- numba is compiling each time that the signature is different, without warning
    or anything:
  - compile `f(1)`
  - compile `f("1")` again
  - compile `f(1.)` again


