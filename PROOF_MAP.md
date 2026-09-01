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
