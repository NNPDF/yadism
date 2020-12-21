Introduction to DIS
===================

History
-------

- Short historical overview "DIS is the process involving [bla bla]"
- "it has been historically relevant in QCD and [bla bla bla]"
- "and it is one of the core element in PDF determination [bla bla bla bla] ..."

Notations
---------

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

Structure Function Kind
-----------------------

``yadism`` allows to compute three different structure functions, to which we refer to as **kind**:

.. math ::
  F_2,~ F_L = F_2 - 2xF_1,~ xF_3

- to compute :math:`F_L` instead of :math:`F_1` is adventagous due to the Callan-Gross relation
  :cite:`Callan:1969uq` :math:`F_L=0` in the naive parton model
- Note that we compute :math:`xF_3` instead of the bare structure function to respect the native
  scaling in the full cross section


Factorization Theorem
---------------------

The choice of the process will affect the coefficient functions, in particular
they will be different for |NC| and |CC|, but the |EM| are exactly the same of
the |NC| (because the diagram are exactly the same for the :math:`\gamma` and
the :math:`Z`).

But coefficient functions are not the only relevant thing about processes,
indeed they will affect also the coupling to the quarks and the relation
between the *hadronic* and *leptonic* part of |DIS|.

.. todo::

   Here a picture made with Inkscape of DIS diagram to make it clear what is
   the hadronic part, what the leptonic and where the coupling are coming into
   the game.

These two further contributions are collected in what we call the **weight**
of each coefficient function (i.e. the weight of each element of the flavor
basis, but we stress that (coefficient functions, processes) and weights are
mapped :math:`1 \leftrightarrow 1`).

In the following the description of the weights for each kind of |DIS| process.

Define the coefficient from *factorization scheme*.

Do we want to include also the perturbative expansion convention? (expand in
``a_s``)

- leptonic
- propagator
- hadronic
- factorization formula contributions
