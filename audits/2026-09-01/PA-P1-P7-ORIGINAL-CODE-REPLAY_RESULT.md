# Property Axiom System 2026-09-01 — independently observed original-code replay

**Author of associated manuscript:** Kwon Dominicus.
Locked printed manuscript: `DSD_Property_Axiom_System_EN(4).pdf` (2026.09.01; 23 pages; SHA256 `03a7e5693b73f0332e71a5eb83483e4f3539fc940d5368d5eec1523867e3d79c`).
[Precommit](PA-P1-P4-ORIGINAL-CODE-REPLAY_PRECOMMIT.md) committed as `60867f848dd301dce94daf0ddb17de0aab832812` before the CI run.

## Actual 2026-10-22 KST GitHub Actions execution
[Run #39733865420](https://github.com/dominicus9708/Property_Axiom_System/actions/runs/39733865420), event `push` on the precommit above, `status=completed / conclusion=success`.
- **Python 3.12:** job `119674906726`, reproducibility and tests both success, **7/7 tests passed**; logs explicitly confirm primitive I/II isolating countermodels, one-input full model, status separation, branches, compression, optional-representation split, and forward-map finite chain.
- **Python 3.10:** job `119674906804`, same steps success and **7/7 tests passed**.
- Previous success `37323340122` on 2026-10-05 is historical and not passed off as this execution.

Original files **unchanged**:
- `src/property_axiom_reproduction.py` blob `04844beca113c24267660fcbb09bc8f833403a28`
- `src/verify_property_axiom_results.py` blob `18f48c15e142a8da2b8c283404ab1fd0d0c262d2`
- `tests/test_property_axiom_reproduction.py` blob `8ba18051a84c8ea913d5773139674e3aba0749a3`

Stored original `results/property_witness_summary.json` contains first branch profiles:
- Stage2: comparison counts `I1=1, I2=I3=I4=I5=0`;
- Stage3: `I1=I2=2, I3=I4=I5=0`;
- Stage4: `I1=I2=I3=2, I4=I5=0`;
- compression equality per property (`domain 2/zero 1/nonzero 1`) despite strict-core-isomorphism false.

The CI run regenerated JSON/CSV inside disposable runners; the workflow did not publish these as separate downloadable artifacts nor commit refreshed outputs. The result is based on **observed step logs**, not a fabricated new artifact.

## New source-specific FPA caveats

The [DSD Method Family 2026-09-01 general Property audit](https://github.com/dominicus9708/DSD_Method_Family/tree/main/DSD_Audit/audits/formal_proof/property_axiom_system/versions/2026-09-01) finds two manuscript text-level issues that the existing finite tests do **not** cover:
1. Definition 6.1 F3–F5 must specify what happens for **declared but source-profile-unavailable** kinds, permitted by Definition 2.5, to keep category identity maps well typed.
2. Theorem 6.8's shorthand “strict isomorphisms exactly bijective property embeddings” must include equal declarations and available-sort sets, not just carrierwise bijective component maps.

This is **not** a failing finite Python regression and is not evidence that the two core soundness axioms or the finite examples should be discarded. Software outputs pass; full-paper source mathematical FPA remains OPEN. No manuscript/Zenodo/Python code changed.

### Windows 11 replay from existing repository root
```powershell
python src\property_axiom_reproduction.py --output-dir results
python src\verify_property_axiom_results.py --results-dir results
python -m unittest discover -s tests -v
```
Existing outputs: `results/property_witness_summary.json`, `results/proof_obligation_audit.json`, `results/witness_catalog.csv`. No external input files.
