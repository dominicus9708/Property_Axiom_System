# Property Axiom System — independent replay and negative-control audit (2026-10-24 KST)

**Author:** Kwon Dominicus.
**Frozen canonical manuscript:** `DSD_Property_Axiom_System_EN(4).pdf`, manuscript printed 2026.09.01, 23 pages, SHA256 `03a7e5693b73f0332e71a5eb83483e4f3539fc940d5368d5eec1523867e3d79c`.
**Scope:** rerun actual previously developed Python unchanged, inspect invariants, compare all committed results, and exercise deliberately adversarial typed inputs. The tests do **not** prove all general set-theoretic theorems or fix the printed §6 conditions.

## 1. Original source custody — actual Git blob lock

No edit to original `src/`, `tests/`, `results/` files:
- `src/property_axiom_reproduction.py`: `04844beca113c24267660fcbb09bc8f833403a28`.
- `src/verify_property_axiom_results.py`: `18f48c15e142a8da2b8c283404ab1fd0d0c262d2`.
- `tests/test_property_axiom_reproduction.py`: `8ba18051a84c8ea913d5773139674e3aba0749a3`.

New *supplementary, non-destructive audit files only*:
- [Negative-control script](PA-REPLAY-20261024_NEGATIVE_CONTROLS.py).
- [Dedicated GitHub Actions workflow](../../.github/workflows/property_replay_audit_20261024.yml); existing `.github/workflows/reproducibility.yml` also triggered on push and unchanged.

## 2. Actual fresh CI executions on both Python versions

- [Existing original workflow #39977127410](https://github.com/dominicus9708/Property_Axiom_System/actions/runs/39977127410): **completed / success**, 7 original `unittest` tests on Python 3.10 and 3.12; original source and code unchanged.
- [Initial independent audit workflow #39977127221](https://github.com/dominicus9708/Property_Axiom_System/actions/runs/39977127221): **completed / success** on 3.10, 3.12; regenerated witness files, original verifier, 7 original tests, **9/9 expected negative-control detections**.
- **Strict byte-for-byte fixture comparison** [#39977709753](https://github.com/dominicus9708/Property_Axiom_System/actions/runs/39977709753): **FAILED on both 3.10/3.12**, intentionally preserving evidence of two archived output byte differences. The original reproduction and 9 negative checks still ran and passed.
- **Corrected evidence classification** [#39977845896](https://github.com/dominicus9708/Property_Axiom_System/actions/runs/39977845896): **completed / success on both Python 3.10 and 3.12**; parsed JSON objects and CSV rows from **all three freshly regenerated outputs matched historical committed fixtures exactly**. 7 original tests and 9/9 negative controls passed again. No original fixture or original source code was changed.

## 3. Important distinction: byte-identical vs mathematically identical saved results

| Previously committed file | Semantic replay | Byte replay | Diagnosis |
| --- | --- | --- | --- |
| `results/property_witness_summary.json` | **PASS** JSON parsed objects equal | **DIFFERENT** | Committed JSON uses compact inline nested structures, original current `json.dumps(..., indent=2)` expands them: committed **1,835 bytes**, regenerated **2,251 bytes**. |
| `results/proof_obligation_audit.json` | **PASS** | **PASS** | Byte-for-byte identical. |
| `results/witness_catalog.csv` | **PASS** parsed CSV rows equal | **DIFFERENT** | Committed and freshly written line-ending representation differs; committed **1,074 bytes**, regenerated **1,084 bytes** for **10 lines**. |

The CSV difference of exactly 10 bytes corresponds to CRLF vs LF over the same 10 CSV records. It does not represent a different witness/result. The JSON differences are whitespace/indentation only. **The strict-byte audit failure was real and preserved**, then the semantic replay classification passed with a narrower, explicitly stated test. Do not report “all three output files are bit-for-bit reproduced.”

## 4. Independent negative-control results (9/9 detections)

The committed extra script executes the **unchanged** original model class and verifier against disposable temporary files. Nine *expected findings* passed in both Python versions:

| Negative control | Actual observed result and scope |
| --- | --- |
| Untyped applicability set member | `is_core_model()` returns `True` even when `Ap_p` includes an input tuple `('ghost',)` outside `X_A,p`. |
| Untyped prerequisite-satisfaction set member | `is_core_model()` returns `True` even when `Sat_{p,d}` includes an input tuple outside the typed product. |
| Declared but unavailable profile with surplus assignment metadata | Unavailable kind can carry extraneous assignment data in Python without raising. Source says coordinates are **not required** here; whether surplus data are forbidden or ignored is a separate modeling/presentation decision, not automatically a source theorem counterexample. |
| Countermodel4.1 raw status overlap | Defined assignment exists while input is inapplicable; `status()` chooses `inapplicable`, masking the simultaneous raw `defined` predicate. |
| Countermodel4.2 raw status overlap | Defined assignment exists while prerequisite unsatisfied; `status()` chooses `prerequisite-unsatisfied`. |
| Countermodels not admitted cores | Both 4.1/4.2 deliberately fail `is_core_model()`; they are premodels and do not refute well-formed full-core C1 status partition. |
| Original verifier accepts clean regenerated outputs | `src/verify_property_axiom_results.py` returns 0. |
| Original verifier misses a tampered status witness | Tampering `status_separation['a']` in a **temporary** generated summary still yields verifier exit code 0. |
| Original verifier trusts contradicted `all_checks_pass` | If a temporary `proof_obligation_audit.json` has an individual `checks` member `False` while `all_checks_pass=True`, verifier still returns 0. |

### Audit interpretation (do not falsely “solve” by changing source)
1. **CODE-VALIDATION-COVERAGE GAP:** `PropertyModel.is_core_model()` implements `PI and PII`, but is **not a comprehensive typed-premodel validator**: it assumes admissible typed primitive sets. Thus its name should not be interpreted as a guarantee about arbitrary user-supplied Python data.
2. **CODE-RESULT-VERIFIER-COVERAGE GAP:** `verify_property_axiom_results.py` checks presence and a small selection of regressions, but does **not** independently recompute every detailed witness or recompute `all_checks_pass` from its flags. Its green exit code is weaker than “all result contents verified.”
3. **CODE-STATUS-SCOPE GAP:** premodel counterexamples not satisfying axioms may have overlapping raw status predicates, while a priority-ordered status function yields one label. This corroborates P14's `Th4.3 relative to C1` proof-scope question; **not** a claim that complete admitted property-core statuses overlap.
4. **BENIGN BYTE-LEVEL FORMAT NONPARITY:** historical JSON/CSV archived formatting differs from deterministic regeneration; all logical values and rows matched in both Python versions.

None of these results refutes Primitive Axioms I and II as general mathematical statements. The printed manuscript's earlier **two separate §6 mathematical condition issues** remain **OPEN** (source-declared profile unavailable guard, and abbreviated bijective embedding vs strict S1–S4).

## 5. Existing Windows 11 replay commands (from established repo root)

```powershell
python src\property_axiom_reproduction.py --output-dir results
python src\verify_property_axiom_results.py --results-dir results
python -m unittest discover -s tests -v
python audits\2026-09-01\PA-REPLAY-20261024_NEGATIVE_CONTROLS.py
```

**Warning:** the first command overwrites the current local `results/` files with newly formatted versions. To preserve the historical byte formatting, run on a clean checkout or worktree and compare parsed JSON objects/CSV rows (as CI does), rather than assuming unchanged file hashes.

## 6. Verdict and non-edit next gate

```text
CASE: PA-REPLAY-20261024-ORIGINAL-AND-NEGATIVE-AUDIT
EXISTING_GENERATOR_VERIFIER_TEST_BLOBS: UNCHANGED
PYTHON_3_10_ORIGINAL_7_TESTS: PASS
PYTHON_3_12_ORIGINAL_7_TESTS: PASS
NEW_NEGATIVE_DETECTIONS: 9/9 BOTH PYTHON
ORIGINAL_RESULT_FILES_SEMANTICALLY_IDENTICAL: 3/3
ORIGINAL_RESULT_FILES_BYTE_IDENTICAL: 1/3
HISTORICAL_BYTE_TEST_FAILURE: PRESERVED
MODEL_TYPING_COMPLETENESS: NOT VERIFIED / COUNTERINPUT FOUND
VERIFIER_ALL_CONTENTS_RECOMPUTATION: INCOMPLETE / TAMPER MISSED
PRINTED_GENERAL_PROPERTY_FPA: OPEN
MANUSCRIPT_OR_ORIGINAL_SRC_TEST_RESULT_EDITED: NO
NEXT: PA-P15-C1-SEMTANTICS AND CODE_VALIDATION_STRENGTHENING / NOT_EXECUTED
```
