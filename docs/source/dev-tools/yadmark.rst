Yadmark
=======

Here we describe the design and API of the `yadmark` package.
The specific purpose of this package is to cointain all the utils to benchmark efficiently `yadism`. 
The underlying infrastructure is coming from `sqlite3` and `git-lfs` and it 
is implemented in the package |banana|.

.. admonition:: Tools

   Other tools have been developed for benchmarking, and shipped with banana as
   CLI. They install together with it, find the description at |banana-tools|. 

To install `yadmark` you can type: 

``pip install yadmark``

.. important::

   Due to a problem in |banana| the only working version of yadmark can be insalled locally 
   with:
   
   ``cd benchmarks && pip install -e .``


There is not an explicit dependency of `yadmark` to |lhapdf|, but to install the external modules it is
needed to have intelled at least the ``lhapdf`` python module.
Among the external programs  olny |APFEL| provides a python wrapper, while both |QCDNUM| and |xspace-bench| 
bindings are available in: `N3PDF/external <https://github.com/N3PDF/external>`_
 

Yadmark is composed by three subpackages:

* ``benchmark`` containing the runner, implementing the interface with the abstract class provided inside |banana| and the external utils that initialise and compute the requested |SF| using the external programs.
* ``data`` which includes the module to generate `yadism` like observables cards and the module providing the observable database layout.
* ``navigator`` implementing the navigator app. 

The banana configuration is loaded from ``banana_cfg.py`` file. 

To run Yadmark see the section of the available :doc:`runners<yadmark_runners>`.
Furthermore Yadmark provides also a python interpter called :doc:`navigator<navigator>` to inspect 
the cached benchmark reuslts. 

.. toctree::
   :maxdepth: 1

   yadmark_runners.rst
   navigator.rst
   API <yadmark/yadmark.rst>






