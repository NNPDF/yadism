# The plan is:
#     - restrict domains of input fields
#     - implement further restrictions (cross-fields)
#     - apply default
#     - suggest fallbacks
#         - probably is better not to directly implement fallbacks as in APFEL and
#           raise an error consistently if something is not allowed, completely
#           avoiding reporting input (they are exactly the one put in by the user)
#
# make use of the values stored in available.yaml and default.yaml
