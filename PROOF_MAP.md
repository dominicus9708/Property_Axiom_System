# Computational proof map

This map states what each executable check supports and what remains a manuscript proof.

| Manuscript result or construction | Executable support | Scope |
|---|---|---|
| Primitive Axiom I countermodel | `construct_pi_countermodel()` | Checks the displayed one-input model with PI false and PII true |
| Primitive Axiom II countermodel | `construct_pii_countermodel()` | Checks the displayed one-input model with PI true and PII false |
| Mutual primitive non-derivability | both countermodel constructors | Reproduces the finite witness pair; the general metatheoretic non-derivability statement remains a manuscript argument |
| One-input nontrivial property model | `construct_one_input_model()` | Checks a finite full model satisfying both primitive axioms and completing to one defined property record |
| Status separation | `construct_status_witness()` | Checks finite instances of inapplicable, prerequisite-unsatisfied, applicable-undefined, defined-zero, and defined-nonzero statuses |
| Unique explicit completion | `PropertyModel.completion()` on finite witnesses | Recomputes derived domains, dependency intersections, statuses, and defined records for the finite witnesses; general uniqueness remains a manuscript proof |
| Stage-2 declaration branch | `construct_stage2_branch()` + exhaustive `stage_comparison_families()` | Exhaustively enumerates the finite carrier bijections and derives first branch 2 |
| Stage-3 applicability branch | `construct_stage3_branch()` + exhaustive `stage_comparison_families()` | Exhaustively enumerates the finite carrier bijections and derives first branch 3 |
| Stage-4 assignment branch | `construct_stage4_branch()` + exhaustive `stage_comparison_families()` | Exhaustively enumerates the finite carrier bijections and derives first branch 4 |
| No independent Stage-5 branch | Stage-4/Stage-5 comparison counts for displayed witnesses | Confirms equality for the finite witness family; the general identity `I_4 = I_5` follows from the manuscript's completion theorem |
| Strict core non-isomorphism of the compression pair | `strict_core_isomorphic()` | Exhaustively rules out all finite carrier bijections for the displayed two-point pair |
| Simple-summary collision | `simple_summary()` on the Stage-4 pair | Reproduces equal per-property domain/zero/nonzero counts despite strict core non-isomorphism |
| Abstract versus represented comparison | finite representation split in `build_summary()` | Shows a displayed core-equivalent pair with unequal optional encodings; general representation-inclusive equivalence remains a manuscript theorem |
| Forward-map composition | `construct_forward_map_chain()`, `is_forward_map()`, `compose_carrier_maps()` | Checks one finite identity-preserving composition instance; category closure in general remains a manuscript proof |
| Property embeddings and submodel preorder | none | General injective/reflection and preorder proofs remain in the manuscript |
| Strict core equivalence relation | finite bijection search only | General identity/inverse/composition proof remains in the manuscript |
| Branching symmetry and strict-isomorphism invariance | finite branch profiles only | General theorem remains in the manuscript |
| Standard finite realization | displayed finite models and completion checks | General sufficiency theorem for arbitrary compatible finite primitive data remains in the manuscript |
| Stage-VI factorization boundary | fixed-background assumption in all constructors | Formation provenance is held fixed; the general interface theorem remains a manuscript statement |

The executable package is therefore a reproducibility and proof-audit companion, not an automated formalization of the entire Property Axiom System.

## Supplemental current P27 audit (2026-10-27; **not** part of historical release 1.1)

The original proof-map table above applies only to the deterministic September 2026 source implementation. It does **not** test the general typed-profile/embedding requirements of revised Property P27.

| P27 revised mathematical obligation | New independent code | Exact applicability and limits |
|---|---|---|
| Stage-VI-fixed typed availability distinctions | `audits/2026-10-27/p27_independent_math.py` | Adversarial missing sort versus supplied empty carrier; one auxiliary sort only |
| Correct S2/S3 strict comparison boundaries | same checker | Constructed forward source embeddings with extra target declaration or availability; not strict |
| E1 applicability when prerequisite set empty | same checker | Independent applicability reflection remains required even if E2 is vacuous |
| Strict isomorphism vs `I_4` | same checker | 396,898 ordered same-size small-model pair checks; general signature theorem remains manuscript proof |
| Deterministic C1 and `I_4=I_5` | same checker | 672 cores and 1,266 stage-4/5 equivalent comparison pairs; finite only |
| Label-retaining simple summary | Existing historical `simple_summary()` dictionary keyed by property name plus independent P27 checker | Must restrict mathematical Def9.1 to declared zero-bearing, profile-available property-finite models; old code itself does **not** validate that typing domain |
| Two primitive axioms / independence | Original one-input constructors plus independent typed counterpremodels | Witnesses show nonderivability over appropriate shared typed-premodel backgrounds, not every fixed signature |

Use [2026-10-27 full compatibility and release audit](audits/2026-10-27/P27_LEGACY_RELEASE_AND_CURRENT_PAPER_COMPATIBILITY.md) and [archived independent P27 results](audits/2026-10-27/p27_expected_result.json) for exact scope. General set-theoretic proof obligations, external peer evaluation and whole FPA remain **OPEN**.
