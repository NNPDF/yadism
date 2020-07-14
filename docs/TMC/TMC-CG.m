(* ::Package:: *)

(* ::Input:: *)
(*(* definitions *)*)
(*r[x_,\[Rho]_]:=Sqrt[1+4x^2 \[Rho]]*)
(*\[Xi][x_,\[Rho]_]:=2x/(1+r[x,\[Rho]])*)
(*\[Tau][x_,\[Rho]_]:=r[x,\[Rho]]^2*)


(* ::Input:: *)
(*(* Schienbein: Eq. 26 of arXiv:0709.1775 *)*)
(*fLs[x_,\[Rho]_] := x^2/\[Xi][x,\[Rho]]^2/r[x,\[Rho]]*fL0[\[Xi][x,\[Rho]]]+4\[Rho] x^3/r[x,\[Rho]]^2h2[\[Xi][x,\[Rho]]]*)


(* ::Input:: *)
(*(* NNPDF/APFEL: (corrected) Eq. 85 of arXiv:0808.1231 *)*)
(*fLa[x_,\[Rho]_]:=fL0[\[Xi][x,\[Rho]]]+x^2(1-\[Tau][x,\[Rho]])/\[Tau][x,\[Rho]]^(3/2)/\[Xi][x,\[Rho]]^2f20[\[Xi][x,\[Rho]]]+2\[Rho] x^3(3-\[Tau][x,\[Rho]])/\[Tau][x,\[Rho]]^2 h2[\[Xi][x,\[Rho]]]*)


(* ::Input:: *)
(*Series[fLs[x,\[Rho]],{\[Rho],0,1}]*)
(*Series[fLa[x,\[Rho]],{\[Rho],0,1}]*)



