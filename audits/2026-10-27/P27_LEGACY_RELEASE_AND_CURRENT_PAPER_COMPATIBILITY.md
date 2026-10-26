# P27 vs released Property Axiom System GitHub — non-destructive compatibility audit

Date: 2026-10-27 KST. Author: Kwon Dominicus.
Repository: `dominicus9708/Property_Axiom_System`.
Current revised research line: `dominicus9708/DSD_Method_Family`.

## Historical release must remain identifiable

- Existing GitHub release [1.1](https://github.com/dominicus9708/Property_Axiom_System/releases/tag/1.1) was published 2026-09-01; its Git tag points to commit `da2db048af072ea194c37d4b6276f4a6fe02f206`.
- The repo's standard-library `src/property_axiom_reproduction.py`, `src/verify_property_axiom_results.py`, `tests/test_property_axiom_reproduction.py`, historic result fixtures and older failed/successful CI checks are **historical evidence**. They are NOT edited by this audit.
- The original published manuscript contains later-identified §4 and §6 math-scope issues. The release description's bare phrase “exactly the bijective embeddings” is NOT a valid characterization without availability- and declaration-set equality; see below. An historical release remains archived, not silently altered.
- Existing `.zenodo.json` metadata describes the historical software companion, not the newly published P27 research edition. A new GitHub tag or automatic Zenodo software release was NOT created.
- Existing `CITATION.cff` identifies the **software companion as `0.1.0`**, whereas GitHub release tag `1.1` is titled for the **paper**. These may denote different version axes and are **not necessarily erroneous**; document the distinction explicitly if issuing a future separate software/paper release, rather than rewriting historical tags automatically.
- The exact original **general** Property Axiom System Zenodo manuscript DOI has not been independently established by this GitHub-only audit. Do not substitute the separate realized-axis specialized DOI, and do not invent a DOI.

## Required interpretation update

| Topic | Legacy code / record | Current P27 manuscript and correct claim | Decision |
|---|---|---|---|
| Primitive soundness and C1 | One-input witnesses and finite derived statuses | PI, PII unchanged. C1 applies to cores satisfying both; independence counterexamples are typed **premodels** | KEEP released code, reference P27 |
| Available sorts / profile guard | `input_product()` returns empty set when a source profile is unavailable, and `is_forward_map()` loops vacuously | P27 §6 (F3)–(F5) explicitly quantifies only source-declared, available profiles; unavailable sort is not the same type state as a supplied empty carrier | KEEP historical finite examples, label code scope LIMITED |
| Property embedding | No general released `is_property_embedding()` exists in `src/` | P27 Def6.3 has distinct applicability E1, per-prerequisite E2, and assignment-domain E3 reflection; all necessary even when prerequisites are empty | ADD independent P27 verifier; do not claim source implements general embedding |
| Strict property isomorphism | Exhaustive finite carrier bijection comparison for displayed witnesses | Theorem6.8 strict iff an embedding plus S1 bijective carrier maps, S2 same available sorts and S3 same declared kinds; S4 inverse then follows | KEEP historical cases; cite corrected theorem and negative witnesses |
| First branching and C1 | Finite S2/S3/S4 branch examples | I4=I5 by deterministic C1; full infinite-set proof remains a manuscript argument | KEEP code, add independent bounded stress test |
| Simple summary | `simple_summary` stores each property's counts under its own name in `properties` dictionary | P27 Def9.1 now also labels each tuple; **defined only for property-finite cores with all declared kinds zero-bearing and their typed profiles available** | NO label-code rewrite needed; document domain restriction explicitly |
| Formation Stage-VI interface | Historical source treats Formation record as immutable backdrop | Formation 2026-10-22 v4.5 Stage VI and Property P27 compatibility checked separately in DSD_Method_Family P22/P23 | LINK independent research record, do not assert released code models all Stage-VI data |

## New independent regression add-on — historical outputs unchanged

- [2026-10-27 P27 checker](p27_independent_math.py) copied from the audited P27 research source in `DSD_Method_Family`.
- [Archived expected P27 JSON](p27_expected_result.json). It records **672 finite cores**, **396,898 same-size ordered model pair checks**, and declared finite countermodels for S2, S3, unavailable profiles, empty prerequisites and historical unlabelled summary collisions.
- [Dedicated GitHub Actions workflow](../../.github/workflows/property_p27_current_audit.yml) tests Python 3.10 and 3.12. It asserts **original source git blob hashes unchanged**, reconstructs three original JSON/CSV fixtures and checks semantic equality, runs the seven original unit tests, executes the P27 checker and requires an exact full JSON match with archived evidence.
- This proves reproducibility of explicitly finite computations only. The P27 suite uses **one auxiliary sort, carrier size 0/1/2, two property kinds and 0/1 values**; no inference to arbitrary signatures, infinite carriers, whole ZFC proof or universal Formation semantics is warranted.

## Related precise current research evidence

- [P27 full math proof-obligation and finite-check report](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/property_axiom_system/versions/2026-09-01/P27_independent_math_revision/P27_INDEPENDENT_MATH_AUDIT_KR.md).
- [Current P27 English TeX candidate](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/property_axiom_system/versions/2026-09-01/P27_independent_math_revision/DSD_Property_Axiom_System_EN_P27_REVISED.tex).
- [Current P27 Korean TeX candidate](https://github.com/dominicus9708/DSD_Method_Family/blob/main/DSD_Audit/audits/formal_proof/property_axiom_system/versions/2026-09-01/P27_independent_math_revision/DSD_Property_Axiom_System_KR_P27_REVISED.tex).
- The original and P27 printed PDFs, current generalized Property Zenodo publication record, and the GitHub historical 1.1 release remain distinct versioned artifacts.

## Remaining work / publication gate

1. Decide when/if the P27 bilingual manuscript becomes a new Zenodo version; verify the original generalized Property DOI and historical record's GitHub related-identifier linkage first.
2. If a **new software release** of the companion is warranted, align `.zenodo.json`, `CITATION.cff`, version number, notes and release tag simultaneously; do not repoint a historical tag or pretend a current audit is the September release.
3. Independent mathematics: multi-sort signatures, missing/supplied-empty carrier boundaries, source-available/target profiles, empty and mixed prerequisite sets, strict inverse across all typed domains, and representation/summary scope. Existing P27 finite tests are not a complete general formal proof.
4. Independent external review and formalized proofs remain OPEN.

Status: `LEGACY_REPRODUCIBILITY_PRESERVED / P27_SUPPLEMENT_ADDED / NO_ZENODO_RELEASE / GENERAL_FPA_OPEN`.
