:orphan:

.. define custom roles and other site-wide stuffs


.. ----
   code
   ----

.. role:: py(code)
   :language: python

.. role:: bash(code)
   :language: bash


.. ----------
   references
   ----------

..  .. role-- eq

.. ----------
   custom css
   ----------

.. raw:: html

   <style type="text/css">
     span.underlined {
       text-decoration: underline;
     }
   </style>

.. role:: underlined
   :class: underlined

.. :underlined:`test`


.. raw:: html

   <style type="text/css">
     span.eqref:before {
       content: "Eq. (";
     }
     span.eqref:after {
       content: ")";
     }
   </style>

.. role:: eqref
   :class: eqref
