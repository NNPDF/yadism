---
documentclass: standalone
classoption:
  - preview
  - border=20pt
header-includes: |
   \usepackage{physics}
   \newcommand{\bps}{\bra{\psi}}
   \newcommand{\kph}{\ket{\phi}}
---
<!--compile with:-->
<!--pandoc -s -o q_{ns}.pdf q_{ns}.md-->

$$ q_{ns} = \sum_q e_q^2 (q + qbar) $$

$$ c_{ns} * q_{ns} + <e^2> * (c_{ns} + c_{ps})*q_s $$

$$ c_{ns} * ( \sum_q (e_q^2 - <e^2>) q_+ ) + <e^2> * (c_{ns} + c_{ps})* ( \sum_q q_+) ) $$
$$ \sum_q q_+ ( c_{ns} *  (e_q^2 - <e^2>)  + <e^2> * (c_{ns} + c_{ps}) ) ) $$
$$ \sum_q q_+ ( c_{ns} * e_q^2 + <e^2> * c_{ps} ) ) $$

--


$$ F_2(x) = x \sum_q e_q^2 * q_+(x) $$

$$F_2(x) = x ( q_{ns}(x) + <e^2> q_s(x) )
 = x ( q_{ns}(x) + <e^2> \sum_q q_+(x) )$$

nf=1:
$$ F_2(x) = x e_u^2 u_+(x) =!= x ( q_{ns}(x) + e_u^2 u_+(x) ) $$

$$ q_{ns}(x) = e_u^2 u_+(x) - e_u^2 u_+(x) = 0 $$

nf=2:
$$ 1/x F_2(x) = e_u^2 u_+(x) + e_d^2 d_+(x) =!= q_{ns}(x) + (e_u^2 + e_d^2)/2 ( u_+(x) + d_+(x) ) $$
$$ q_{ns}(x) = e_u^2 u_+(x) + e_d^2 d_+(x) - (e_u^2 + e_d^2)/2 ( u_+(x) + d_+(x) ) $$

=>
$$ q_{ns}(x) = \sum_q (e_q^2 - <e^2>) q_+(x) $$

<!-- vim: set ft=pandoc: -->
