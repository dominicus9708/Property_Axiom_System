# General Property Axiom System P1–P4 unchanged-code CI replay — preregistration
Audit date 2026-10-22 KST. Paper author Kwon Dominicus.
Exact manuscript source: `DSD_Property_Axiom_System_EN(4).pdf`, printed `2026.09.01`, 23 pages, SHA256 `03a7e5693b73f0332e71a5eb83483e4f3539fc940d5368d5eec1523867e3d79c`.

Before observing a newly triggered result, freeze original code blob identities:
- `src/property_axiom_reproduction.py` Git blob `04844beca113c24267660fcbb09bc8f833403a28`;
- `src/verify_property_axiom_results.py` Git blob `18f48c15e142a8da2b8c283404ab1fd0d0c262d2`;
- `tests/test_property_axiom_reproduction.py` Git blob `8ba18051a84c8ea913d5773139674e3aba0749a3`.

The repository's workflow `.github/workflows/reproducibility.yml` has a push trigger and Python 3.10/3.12 matrix. This audit-record-only commit will trigger CI, without modifying original executable source, test inputs, expected values, or deterministic `results/` artifacts.

### Prospective checks
1. Observe *new* workflow run associated with the commit, verify both Python versions completed successfully, inspect detailed job logs for the actual reproduce/verify/unit-test steps.
2. Preserve evidence for the finite witnesses: PI/PII typed countermodels, 5-way definedness/status separation, one-input full property core, Stage 2/3/4 first branching, Stage 4 = Stage 5 on selected finite models, compression/strict-isomorphism separation, representation forgetting and forward map composition.
3. Separate finite executable checks from general proof obligations: typed signature totality, C1 unique completion, inverse laws, morphism category and equivalence, generic finite realization and all stage invariants require source-level mathematical audit.
4. Do not import previously successful 2026-10-05 CI as this new run, and do not invent artifact uploads.
5. Audit scripts remain at the already established paths and write to `results/`. No new arbitrary directories for data inputs/outputs.
6. Preserve specialized realized-axis repo and independent Formation F2 cases untouched.

```text
SOURCE: manuscript 2026-09-01
CI_NEW_RUN: PENDING
ORIGINAL_ALGORITHMS_MODIFIED: no
MATH_FPA: OPEN
```
