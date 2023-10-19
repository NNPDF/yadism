DIS: process and definitions
============================


.. image:: /_static/dis-pink-book.png
   :align: center

The Deep Inelastic Scattering process is the scattering of a lepton over an
hadron component, mediated by an |EW| boson.

The leptonic part does not couple directly to |QCD|, thus the :math:`\alpha_s`
corrections do apply only to the hadronic side (at |LO| |EW|), and the |EW|
boson can be seen as emitted from the incoming lepton and absorbed into the
hadron.

In this picture the process can be interpreted as the scattering of an off-shell
|EW| boson over an hadron, probing the hadron composition.

Kinematics
----------

The following kinematic variables are often used in the following:

.. math::

   Q^2 &= - q^2 \\
   M_h^2 &= p^2 \\
   \nu &= q \cdot p \\
   x &= \frac{Q^2}{2\nu} \\
   y &= \frac{q \cdot p}{k \cdot p}

so :math:`M_h` is the mass of the scattered hadron, while :math:`x` and
:math:`y` are Bjorken variables.

.. admonition:: Hadronic vs Partonic

   Notice that the variables listed here are all **hadronic**, so :math:`x` is
   not the partonic momentum fraction (it is only at |LO|, because the
   coefficient function is a :math:`\delta`).

   In order to avoid confusion the coefficient function variable will be called
   :math:`z`, and thus the partonic momentum fraction will be :math:`x/z`.

Notations
---------

.. figure:: /_static/handbag.png
   :align: center

   The handbag diagram (B(k,p) are the |QCD| corrections to the hadronic tensor)

We are following the notations in :cite:`Zyla:2020zbs`, i.e. we're using their
normalization and definitions. So the hadronic tensor is given by

.. math ::
    W_{\mu\nu} = \left(-g_{\mu\nu} + \frac{q_\mu q_\nu}{q^2}\right) F_1(x,Q^2)
                + \frac{\hat P_\mu \hat P_\nu}{P \cdot q} F_2(x,Q^2)
                - i \varepsilon_{\mu\nu\alpha\beta} \frac{q^\alpha P^\beta}{2 P\cdot q} F_3(x,Q^2)

with :math:`\hat P_\mu = P_\mu - (P\cdot q / q^2) q_\mu`, :math:`P` the 4-momentum
of the hadron and :math:`q` the 4-momentum of the scattered boson.

Process / Currents
------------------

``yadism`` allows to compute three different type of **processes**, which correspond to a
given set of scattering bosons:

- Electromagnetic Current (|EM|): we only allow the photon to be exchanged. This is the
  most basic setup and in many cases the only allowed option.
- Neutral Current (|NC|): in addition to the photon we also allow for the :math:`Z`
  boson to be exchanged, so this is a superset of |EM|.
  Since now two bosons are allowed also interference terms appear.
  The :math:`Z` boson has an axial coupling to the leptons and thus it introduces the problems
  related to :math:`\gamma_5` :cite:`Gnendiger:2017pys`.
  Note that there are no Flavor Changing Neutral Currents (FCNC) in the |SM|, but they are an
  active field of research.
- Charged Current (|CC|): we only allow the :math:`W^+` *or* :math:`W^-` to be exchanged.
  The actual boson is determined by the incoming scattering lepton and charge conservation.
  As the :math:`W^\pm` are flavor changing additional care is needed in the calculation.

.. _kinds def:

Structure Function Kind
-----------------------

``yadism`` allows to compute different structure functions, to which we refer to as **kind**.
In the unpolarized |DIS| we have:

.. math ::

  F_2,~F_L = F_2 - 2xF_1,~xF_3

while their counter parts for the polarized case are:

.. math ::

  g_4,~g_L = g_4 - 2xg_5,~2xg_1

The reasons to chose such basis are:

  - the normalization is such that they have similar representation in the parton model.
    I.e. at |LO| they are all proportional to various combination of :math:`x f(x)`.

    .. math ::

      F_2 & \propto x \sum_q (q + \bar{q}) \\
      x F_3 & \propto x \sum_q (q - \bar{q})

    This normalization also follows the native scaling in the full cross section.

  - computing :math:`F_L` instead of :math:`F_1` is advantageous due to the Callan-Gross relation
    :cite:`Callan:1969uq` :math:`F_L=0` in the naive parton model

  - finally notice that the :math:`F_L` definition it's not exactly the one above, but
    it may be corrected (actually :math:`F_L` it's the object involved in
    Callan-Gross relation, for more information see :ref:`fl-corrections`)

.. note::

   :math:`2xF_1` and :math:`2xg_5` are also provided as they are treated as a derived quantity, like
   the cross sections in the following section.

Cross sections
~~~~~~~~~~~~~~

``yadism`` is also able to compute reduced cross-sections, that are observables
derived from the structure functions themselves.

The cross-section itself is only one, and the structure functions are
simply its components resolved by kinematics, as written above in the
:ref:`hadronic tensor expression <theory/intro:Notations>`.

Instead the reduced cross-sections are many, distinguished by their
normalization, the following are available in ``yadism``:

.. math::

   \sigma = N \left( F_2 - \frac{y_L}{y_+} F_L + (-1)^\ell \frac{y_-}{y_+} x F_3 \right)

- ``XSHERANC`` where:

   .. math::

      N &= 1 \\
      y_+ &= 1 + (1-y)^2 \\
      y_- &= 1 - (1-y)^2 \\
      y_L &= y^2

   and :math:`\ell` is the kind of lepton: :math:`\ell = 0` for the leptons and
   :math:`\ell = 1` for the antileptons.

- ``XSHERACC`` where:

   .. math::

      N = \frac{1}{4} y_+

   and the other variables as above.

- ``XSCHORUSCC`` where:

   .. math::

      N &= \frac{G_F^2 M_h}{2\pi ( 1+ Q^2 / M_W^2 )^2} y_+\\
      y_+ &= 1 + (1-y)^2 - 2 \frac{(x y M_h)^2}{Q^2}

   and :math:`M_h` is the mass of the scattered hadron, the other variables as
   above.
   This definition is consistent also with the ``CDHSW`` experiment.
   Note that a conversion factor from :math:`GeV^{-2} \to cm^2` is required.

- ``XSNUTEVCC`` :cite:`CHORUS:2005cpn`:

   .. math::

      N = \frac{100}{2 ( 1+ Q^2 / M_W^2 )^2} y_+

   the other variables as ``XSCHORUSCC``.

- ``XSNUTEVNU`` :cite:`NuTeV:2005wsg`:

   .. math::

      N = \frac{G_F^2 M_h}{2 \pi } y_+

   the other variables as ``XSCHORUSCC``.
   Also in this case a conversion factor from :math:`GeV^{-2} \to cm^2` is required.

- ``FW`` from the ``CDHSW`` experiment :cite:`Berge:1989hr`:

   .. math::

      N &= 1.0 \\
      y_{-} &= 0 \\
      y_{+} &= 1.0 \\
      y_{L} &= \frac{y^2}{2 (y^2/2 + (1-y) - (M_{h} x y/ Q)^2)}

- ``XSFPFCC`` for the FPF projection:

   .. math::

      N = \frac{G_F^2}{8 \pi x ( 1 + Q^2 / M_W^2 )^2} y_+


Heavyness
---------

All the observables are available in multiple *heavynesses*, that correspond to
the inclusion or less of contributions related to heavy quarks:

- ``total`` is the heavyness that collects all the available contributions,
  according to the |FNS| chosen (see :doc:`fns` for details)
- ``light`` observables contains only contributions from light quarks, so no
  mass effects are accounted for (actually as the massive quarks were infinitely
  massive); in the |ZM-VFNS| it coincides with ``total``
- ``<flavor>``, e.g. ``charm``, contains the contributions in which the heavy
  quark of selected flavor couples directly to the |EW| boson (as if only the
  charge of the given flavor is non-zero, while all the other couplings are set
  to zero)

Notice that the contributions in which the heavy quark is present, but does not
couple to the |EW| boson, are not included nor in ``light`` neither in
``<flavor>``, but they are of course present in ``total``, thus:

.. math::

   O_{total} \neq O_{light} + O_c + O_b + O_t

All the heavynesses are defined tuning parameters at Lagrangian level, thus all
the observables are potential physical observables, since they are well-defined
and free of divergences.

For a more in-depth discussion with the relation of heavyness and |FNS| see
:doc:`fns`.
