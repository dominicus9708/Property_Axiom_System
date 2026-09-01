# Property Axiom System reproducibility package

This repository is the standard-library Python companion to:

> Kwon Dominicus, *Property Axiom System in Dimensional-Structural Describability — A General Typed Property Extension of the Formation Axiom System*.

It reproduces the manuscript's explicit finite countermodels, status-separation witness, finitely specified first-branch witnesses, optional-representation separation, and finite compression obstruction. It does **not** replace the manuscript's general set-theoretic proofs of unique explicit completion, primitive reduction/completion inverse laws, map and embedding closure, strict-equivalence properties, branching invariance, or arbitrary compatible finite-data realization.

This repository is the generalized successor of the property-core portion of `Axioms-for-the-Property-Structure-of-Realized-Axes`. Axis realization, line/rank data, bilinear forms, normals, and cyclic axis closure are intentionally not reproduced here; those remain part of the historical realized-axis specialization and are reserved for later structural-gravity work.

## Reproduced claims

The package deterministically verifies:

- the finite countermodel in which Primitive Axiom I fails while Primitive Axiom II holds;
- the finite countermodel in which Primitive Axiom II fails while Primitive Axiom I holds;
- mutual finite witness support for the non-derivability of the two primitive axioms;
- a one-input nontrivial full property-model witness;
- explicit separation of `inapplicable`, `prerequisite-unsatisfied`, `applicable-undefined`, `defined-zero`, and `defined-nonzero` states;
- a Stage-2 declaration first-branch witness;
- a Stage-3 applicability first-branch witness;
- a Stage-4 assignment first-branch witness;
- exhaustive finite comparison-set counts for those displayed branch witnesses;
- equality of Stage-4 and Stage-5 comparison counts in the displayed finite witnesses, reflecting that explicit completion adds no independent primitive branch;
- a finite collision in the simple property summary while strict core property isomorphism fails;
- a finite example in which strict core equivalence survives while representation-inclusive equivalence fails;
- a finite forward-map chain whose displayed componentwise composition is again a forward property map.

## Requirements

- Python 3.10 or later
- No third-party dependencies

The finite witness data are embedded deterministically in the program. There is no external input file for this formal reproducibility package, matching the companion `Formation_Axiom_System` repository.

## Run on Windows

From the repository root:

```powershell
python src\property_axiom_reproduction.py --output-dir results
python src\verify_property_axiom_results.py --results-dir results
python -m unittest discover -s tests -v
```

## Run on Linux or macOS

```bash
python3 src/property_axiom_reproduction.py --output-dir results
python3 src/verify_property_axiom_results.py --results-dir results
python3 -m unittest discover -s tests -v
```

## Deterministic outputs

- `results/property_witness_summary.json`
- `results/proof_obligation_audit.json`
- `results/witness_catalog.csv`

## Interpretation boundary

The executable package checks the manuscript's explicitly finite instances and finite necessary obstructions. It is not an automated formalization of the whole Property Axiom System. In particular, the general theorems on completion/reduction inverse laws, category formation, embedding closure, property-submodel preorder, strict-isomorphism equivalence, representation-inclusive equivalence, branching symmetry/invariance, and standard finite realization remain manuscript proofs.

The package also does not assign physical, geometric, legal, software, or empirical meaning to a property label. Property kinds are handled only through their declared typed profiles, applicability sets, prerequisite-satisfaction sets, partial assignments, and optional representation data.

## Formation and axis-specialization boundary

The code treats the Stage-VI Formation Axiom System record as fixed background provenance and does not modify formation assignments, roles, admitted channels, or formation traces. The generalized property core does not assume `tag`, `line`, `sub`, `normal`, `AxLine`, realized-axis rank, a bilinear form, or cyclic triadic closure. Those coordinates belong to the separate realized-axis specialization rather than to the universal property core.
