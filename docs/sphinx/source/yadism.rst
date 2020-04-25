.. yadism package

yadism
======

In this section is documented the structure of the package and it's API.

If you were looking for informations about other interesting facts (like
processes description and other physics) check the appropriate section, e.g.
:doc:`physics`.

.. toctree::
   :maxdepth: 2

   API <modules/yadism>


.. todo::

   * add Introduction section

     * include a very brief digraph to expose the overall structure of the
       project

   * add Usage section
   * add Description section

     * put graphs in spoiler tags
     * add to ESF children graphs the corresponding for SF, using a 2-rows table
       (first one for SF, second for ESF, first column F2, second FL)

.. note::
   use this section for stuffs related closely to the package itselg

Introduction
------------
The structure of `yadism` is nice, we are glad that you are reading and we hope
you will like it as much as possible.

Graph placeholder.

Usage
-----
Brief description on how to use yadism, for detailed explanation look
`Description`_

Description
-----------
Some blabla about the yadism package: purpose, usage, trivia and so on.


.. graphviz::
   :name: structure
   :caption: classes' structure
   :align: center

   digraph G {
      bgcolor = transparent
      layers = "RUN:SF:ESF";

      node [shape=box]
      run [label="Runner" group=main layer=RUN]
      sf [label="Structure Functions" group=main layer=SF pos="0,2!"]
      esf [label="Evaluated Structure Functions" layer=ESF group=main]

      node [shape=egg pin=true]
      f2 [label="F2" pos="1,1!" layer=SF group=sfsub]
      fL [label="FL" layer=SF group=sfsub]
      esf2; esfL;
      dvec [label="DistributionVec" shape=polygon sides=9]

      node [shape=ellipse,style=filled,color=white,width=0,height=0,fontsize=8];
      l2 [label=l]; c2 [label=c]; b2 [label=b]; t2 [label=t];
      lL [label=l]; cL [label=c]; bL [label=b]; tL [label=t];

      // aux nodes
      node [style=invis]
      il1

      {rank=same il1 f2 fL}

      run -> sf [arrowhead=odot style=dotted]
      sf -> il1 -> esf [style=invis]
      sf -> esf [arrowhead=odot style=dotted]
      sf -> {f2 fL}
      esf -> {esf2 esfL}
      esf -> dvec [arrowhead=onormal style=dashed]
      esf2 -> {l2 c2 b2 t2}
      esfL -> {lL cL bL tL}

      subgraph clusterF2flavours {
         style="rounded";
         bgcolor=lightgrey;
         {l2 c2 b2 t2};
         subgraph clusterF2Hflavours {
            style="rounded";
            bgcolor=transparent;
            {c2 b2 t2};
         }
      }
      subgraph clusterFLflavours {
         style="rounded";
         bgcolor=lightgrey;
         {lL cL bL tL};
         subgraph clusterF2Hflavours {
            style="rounded";
            bgcolor=transparent;
            {cL bL tL};
         }
      }
   }


Structure Functions flavors
^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. list-table:: An example caption
   :widths: 10 10
   :header-rows: 0
   :stub-columns: 0

   * - .. graphviz::
         :name: F2
         :caption: F2
         :align: center

         digraph G {
            bgcolor = transparent

            node [shape=box]

            f2 [label=F2]
            f2h [label=F2Heavy]

            subgraph F2flavors {
               node [shape=ellipse]
               f2 -> {light, f2h}
               f2h -> {charm, bottom, top}
            }
         }
     - .. graphviz::
         :name: FL
         :caption: FL
         :align: center

         digraph G {
            bgcolor = transparent

            node [shape=box]

            fl [label=FL]
            flh [label=FLHeavy]

            subgraph FLflavors {
               node [shape=ellipse]
               fl -> {light, flh}
               flh -> {charm, bottom, top}
            }
         }

..
   main -> parse -> execute;
   main -> init;
   main -> cleanup;
   execute -> make_string;
   execute -> printf
   init -> make_string;
   main -> printf;
   execute -> compare;1

