# Input subpackage

## inspector.py

### todo

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

## domains.yaml

- add all the parameters' (inputs) domains here
  - included the ones not present in the "theory"
    - should be almost all (theory is mostly responsibility of 'eko')
  - included arguments not present in APFEL
    - or present in another way in APFEL

### lower priority

- add descriptions to all
