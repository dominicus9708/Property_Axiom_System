# Reproducibility protocol

## Scope

This package is designed to reproduce only finite constructions and finite obstructions explicitly used by the Property Axiom System manuscript. General set-theoretic theorems remain manuscript proofs.

## Environment

- Python 3.10+
- Python standard library only
- No external datasets
- No random seeds or nondeterministic sampling

## Inputs

There are no external runtime input files. The formal finite witnesses are encoded directly in `src/property_axiom_reproduction.py` so that the executable objects match the manuscript constructions.

## Outputs

Running the reproduction command rewrites the following deterministic files:

- `results/property_witness_summary.json`
- `results/proof_obligation_audit.json`
- `results/witness_catalog.csv`

`verify_property_axiom_results.py` treats the JSON audit and the displayed first-branch/compression regressions as executable obligations. The unit tests independently exercise the principal constructors and comparison routines.

## Windows commands

```powershell
python src\property_axiom_reproduction.py --output-dir results
python src\verify_property_axiom_results.py --results-dir results
python -m unittest discover -s tests -v
```

## Interpretation

A passing run means that the encoded finite witnesses reproduce the stated finite consequences. It does not establish the general completion theorem, category or equivalence theorems, first-branching invariance, empirical adequacy, or the validity of any later physical specialization.
