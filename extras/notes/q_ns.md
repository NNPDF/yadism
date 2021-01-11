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
<!--pandoc -s -o q_ns.pdf q_ns.md-->

q_ns = sum_q e_q^2 (q + qbar)

c_ns * q_ns + <e2> * (c_ns + c_ps)*q_s

$$ c_ns * ( sum_q (e_q^2 - <e2>) q_+ ) + <e2> * (c_ns + c_ps)* ( sum_q q_+) ) $$
$$ sum_q q_+ ( c_ns *  (e_q^2 - <e2>)  + <e2> * (c_ns + c_ps) ) ) $$
$$ sum_q q_+ ( c_ns * e_q^2 + <e2> * c_ps ) ) $$

--


$$ F_2(x) = x sum_q e_q^2 * q_+(x) $$

F_2(x) = x ( q_ns(x) + <e2> q_s(x) )
 = x ( q_ns(x) + <e2> sum_q q_+(x) )

nf=1:
$$ F_2(x) = x eu^2 u_+(x) =!= x ( q_ns(x) + eu^2 u_+(x) ) $$

$$ q_ns(x) = eu^2 u_+^(x) - eu^2 u_+^(x) = 0 $$

nf=2:
$$ 1/x F_2(x) = eu^2 u_+(x) + ed^2 d_+(x) =!= q_ns(x) + (eu^2 + ed^2)/2 ( u_+(x) + d_+(x) ) $$
$$ q_ns(x) = eu^2 u_+(x) + ed^2 d_+(x) - (eu^2 + ed^2)/2 ( u_+(x) + d_+(x) ) $$

=>
$$ q_ns(x) = sum_q (eq^2 - <e2>) q_+(x) $$

<!-- vim: set ft=pandoc: -->
