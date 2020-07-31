DIS introduction
================

- Short historical overview "DIS is the process involving [bla bla]"
- "it has been historically relevant in QCD and [bla bla bla]"
- "and it is one of the core element in PDF determination [bla bla bla bla] ..."

Overview of coefficient functions structure
-------------------------------------------

The main categories for coefficients functions are of course:

- the **process** (EM/NC/CC)
- the **structure function** (F2/L/3)
- the **flavor** involved (light/charm/bottom/top)

These options set the overall structure of the coefficient functions, and it is
reported in the following tables, just considering that all the heavy flavors
(charm/bottom/top) share the same functional form for the coefficient and a
further category (the massless limit of the heavy) is needed for variable
flavor scheme like FONLL.

.. csv-table:: NC coefficients
   :file: ./nc-coeffs.csv
   :delim: space
   :header-rows: 1
   :stub-columns: 1
   :align: center


.. csv-table:: CC coefficients
   :file: ./cc-coeffs.csv
   :delim: space
   :header-rows: 1
   :stub-columns: 1
   :align: center

There are two further categories in which the coefficient functions are
organized:

- the **incoming flavor**: this will specify the input PDF to which the
  coefficient applies; usually a single expression applies to multiple PDFs,
  but the actual structure depends on the flavor
- the **parity structure** (vectorial-vectorial/axial-axial/vectorial-axial),
  it is relevant only for the NC

