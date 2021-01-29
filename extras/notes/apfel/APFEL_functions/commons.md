# Commons - APFEL common blocks

## Known

### Single/Small set Variable
Each of the following common blocks contains a single or small set of relevant variables.

Moreover each common block contains one further var 'InX':
initially set to 'xxxx' by `CleanUp` and then to 'done' when the relevant variable is set.

#### DIS
the set function is in the DIS package

- CKM.h: CKM matrix values and their squares
- DampingFONLL.h: damping powers for FONLL (dpc, dpb, dpt)
- EWCouplings.h: EW couplings (VD, VU, AD, AU)
    - they have a default available
- GFermi.h: Fermi coupling constant
- MassScheme.h: mass mass_scheme
    - FFNS, FFNS3, FFNS4, FFNS5, FFNS6
    - FFN0, FFN03, FFN04, FFN05, FFN06
    - others
- kfacQ.h: ratio between DIS and factor scale
- krenQ.h: ratio between DIS and renorm scale
- PolarizationDIS.h: DIS polarization
- ProcessDIS.h: set DIS process kind
- ProjectileDIS.h: DIS projectile kind
- PropagatorCorrection.h: Z propagator correction
- ProtonMass.h: proton mass
- ScaleVariationProcedure.h: This subroutine sets the the procedure to be used to vary factorisation and remormalisation scale
    - 0: consistent scale variation in DIS and evolution 
    - 1: variation only in the DIS structure functions
- Sin2ThetaW.h: theta Weinberg
- TargetDIS.h: DIS target kind
- WMass.h: W mass
- ZedMass.h: zed mass


## Unknown

AlphaEvolution.h, alpha_ref_QCD.h, alpha_ref_QED.h, CheckAPFEL.h, coeffhqmellin.h, ColorFactors.h, consts.h, DISOperators.h, DynScVar.h, EpsTrunc.h, EvolOp.h, EvolutionMatrices.h, EvolutionOperator.h, Evs.h, f0ph.h, FastEvol.h, FKObservable.h, fph.h, fphxQ.h, gridAlpha.h, grid.h, gridQ.h, InAPFELDIS.h, InAPFEL.h, integralsDIS.h, integrals.h, integralsResDIS.h, integralsRes.h, IntrinsicCharm.h, ipt.h, kren.h, lambda_ref_QCD.h, LeptEvol.h, LHAgrid.h, lock.h, m2th.h, MassInterpolIndices.h, MassRunning.h, mass_scheme.h, MaxFlavourAlpha.h, MaxFlavourPDFs.h, minimax.h, Nf_FF.h, NLOQEDCorrections.h, odeint1.h, odeint2.h, PDFEvolution.h, pdfset.h, Polarized.h, Replica.h, scales.h, SelectedCharge.h, Smallx.h, StructureFunctions.h, StructureFunctionsxQ.h, TauMass.h, Th.h, ThresholdAlphaQCD.h, TimeLike.h, TMC.h, transQCD.h, transUni.h, Welcome.h, wrapDIS.h, wrap.h, wrapIC.h, wrapResDIS.h, wrapRes.h 
