# Input subpackage

## inspector.py

### todo

- implement CrossConstraint
  - see cross_constraints.yaml
- implement Defaults

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

- MassScheme is not a cross constraint, so it should be implemented in another
  way (also because otherwise it would fail without any reason)

## domains.yaml

- add all the parameters' (inputs) domains here
  - included the ones not present in the "theory"
    - should be almost all (theory is mostly responsibility of 'eko')
  - included arguments not present in APFEL
    - or present in another way in APFEL

### lower priority

- add descriptions to all

## default.yaml

- define syntax
  - plain defaults (if we want to use them)
  - conditional defaults
    - useful for internals and some relations among inputs, but if they try
      define a default for something that it is already defined differently it
      should raise an error (in this way they become more similar to cross
      constraints than actual defaults)
