---
documentclass: article
classoption:
title: Non-singlet and Singlet PDF definition
subtitle: in "DIS" basis
geometry: "left=3cm,right=3cm,top=2cm,bottom=2cm"
linkcolor: Aquamarine
toccolor: black #darkgray
citecolor: Aquamarine
urlcolor: Aquamarine
filecolor: magenta
header-includes: |
  \usepackage{cleveref}
  \usepackage{physics}
  \newcommand{\bps}{\bra{\psi}}
  \newcommand{\kph}{\ket{\phi}}
---

<!--compile with:-->
<!--pandoc -s -o q_{ns}.pdf q_{ns}.md-->

From Vogt 3-loop paper \cite[eq. $(4.1)$]{vogt-3loop}, we get:

$$
x^{-1} F = C_{ns} \otimes q_{ns} + \ev{e^2} \left(C_q \otimes q_s + C_g \otimes g\right)
$$

where:

$$
C_q = C_{ns} + C_s
$$

## Basis definition

The "singlet" is the actual \emph{flavor singlet}:

$$
q_s = \sum_q  (q + \bar{q})
$$

The so called "non-singlet" is actually the difference between the \emph{charged
singlet} and the \emph{flavor singlet}:

$$
q_{ns} = \sum_q \left(e_q^2 - \ev{e^2}\right) ~ (q + \bar{q})
$$

Of course they are both \emph{singlet-like} (referring to evolution basis) since
they are proportional to $q_+$

$$
q_+ = q + \bar{q}
$$

This basis is natural because NC cannot distinguish a flavor from the
anti-flavor (instead CC can).

### Charged Current

CC can be treated in an analogous way, simply:

- when the incoming quark is _directly_ coupling (_non-singlet_) to the EW boson
  (so $W_{\pm}$) only the flavor or the anti-flavor may have a non-zero
  coupling, but not both
- when the incoming quark is _indirectly_ coupling through a gluon (_singlet_)
  nothing change, because the average has to be done on half the objects, but
  being an average this amounts to multiply and divide by $2$

## Equivalent expression (`yadism`)

An equivalent expression is:

$$
C_{ns} \otimes \left(\sum\nolimits_q e_q^2 ~ q_+\right) +
C_{ps} \otimes \left(\sum\nolimits_q \ev{e^2} ~ q_+\right)\\
$$

so in `yadism` we are using:

- the name **non-singlet** to call the _charged singlet_:
  - in which every quark is weighted with the square of its charge
- the name **singlet** to call the _flavor singlet_:
  - in which every quark is weighted with the average of all the square charges
    of the quark that are taking part

Indeed:

<!-- prettier-ignore -->
\begin{gather}
C_{ns} \otimes q_{ns} + \ev{e^2} (C_{ns} + C_{ps}) \otimes q_s\\
C_{ns} \otimes \left( \sum\nolimits_q (e_q^2 - \ev{e^2}) ~ q_+ \right) +
\ev{e^2} (C_{ns} + C_{ps}) \otimes \left( \sum\nolimits_q q_+\right) \\
\sum\nolimits_q q_+ \otimes ( C_{ns}  (e_q^2 - \ev{e^2}) + \ev{e^2} \* (C_{ns} + C_{ps}) ) )\\
\sum\nolimits_q q_+ \otimes ( C_{ns}  e_q^2 + \ev{e^2} C_{ps} ) )
\end{gather}

## Inducing from LO structure functions

To retrieve the exact definition of $q_{ns}$ in \cite{vogt-3loop} we assumed:

- $q_s = \sum\nolimits_q q_+(x)$, i.e. the _singlet_ is the _flavor singlet_
- and we compare the LO DIS expressions

<!-- prettier-ignore -->
\begin{align}
x^{-1} F_2(x) &=  \sum\nolimits_q e_q^2 ~ q_+(x) \label{eq:lo}\\
x^{-1} F_2(x) &=  q_{ns}(x) + \ev{e^2} q_s(x) \label{eq:vogt-lo}\\
&=  q_{ns}(x) + \ev{e^2} \sum\nolimits_q q_+(x)
\end{align}

Where:

- \cref{eq:lo} is the LO DIS result in the flavor basis
- \cref{eq:vogt-lo} is the way it is expressed in \cite{vogt-3loop}

Consider the following hypothesis on the number of flavors:

- $n_f=1$:

<!-- prettier-ignore -->
\begin{align}
x^{-1} F_2(x) &= e_u^2 ~ u_+(x) \stackrel{!}{=} q_{ns}(x) + e_u^2 u_+(x)\\
&\Rightarrow q_{ns}(x) = e_u^2 u_+(x) - e_u^2 u_+(x) = 0
\end{align}

- $n_f=2$:

<!-- prettier-ignore -->
\begin{align}
x^{-1} F_2(x)  &= e_u^2 u_+(x) + e_d^2 d_+(x) \stackrel{!}{=} q_{ns}(x) +
\frac{e_u^2 + e_d^2}{2} ~ ( u_+(x) + d_+(x) )\\
&\Rightarrow q_{ns}(x) = e_u^2 u_+(x) + e_d^2 d_+(x) - \frac{e_u^2 + e_d^2}{2} ~ ( u_+(x) + d_+(x) )
\end{align}

Then:

$$
q_{ns}(x) = \sum_q (e_q^2 - \ev{e^2}) ~ q_+(x)
$$

\begin{thebibliography}{9}
\bibitem{vogt-3loop}
J.~A.~M.~Vermaseren, A.~Vogt and S.~Moch,
%``The Third-order QCD corrections to deep-inelastic scattering by photon exchange,''
Nucl. Phys. B \textbf{724} (2005), 3-182
doi:10.1016/j.nuclphysb.2005.06.020
\href{https://arxiv.org/abs/hep-ph/0504242}{arXiv:hep-ph/0504242}.
%403 citations counted in INSPIRE as of 11 May 2021
\end{thebibliography}

<!-- vim: set ft=pandoc: -->
