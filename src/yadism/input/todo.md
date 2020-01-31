# Input subpackage

## inspector.py

### todo

- document RealArgument
- format RealArgument domain in _raise_error
- implement CrossConstraint
  - see cross_constraints.yaml

### plan

The plan is:
   - implement further restrictions (cross-fields)
   - apply default
   - suggest fallbacks
       - probably is better not to directly implement fallbacks as in APFEL and
         raise an error consistently if something is not allowed, completely
         avoiding reporting input (they are exactly the one put in by the user)
make use of the values stored in available.yaml and default.yaml

### lower priority

- raise an exception if there is a restriction and the corresponding argument
  is missing in the user input (after implementing internal_repr, otherwise
  it will be plenty of errors)


## cross_constraints.yaml

### domains.yaml

- add descriptions to all
- add a field for the actual name as used in the theory and dis_observables
  (`internal_repr` or something like that)
  - ATTENTION: the `internal_repr` is actually the one provided by the user, while
    the `name` is the one used inside apfel
    -> moved to `known_as` (I still need something better)
