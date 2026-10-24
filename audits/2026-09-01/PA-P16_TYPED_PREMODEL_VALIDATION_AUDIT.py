#!/usr/bin/env python3
"""P16 original PropertyModel implementation vs manuscript typed-premodel contract.

Independent expected-negative controls; original src/, tests/, and results/ unchanged.
Kwon Dominicus, original English property paper 2026-09-01.
Usage from repository root:
  python audits/2026-09-01/PA-P16_TYPED_PREMODEL_VALIDATION_AUDIT.py
  python audits/2026-09-01/PA-P16_TYPED_PREMODEL_VALIDATION_AUDIT.py output.json
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import property_axiom_reproduction as pa

SHA = "03a7e5693b73f0332e71a5eb83483e4f3539fc940d5368d5eec1523867e3d79c"

def audit():
    tests = {}
    witness = {}
    sig = {"p": pa.PropertySpec(("u",), ("d",), zero=0, zero_bearing=True)}
    x = ("x",)
    true_core = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",),
        {"p": {x}}, {("p", "d"): {x}}, {"p": {x: 0}})
    tests["positive_valid_core_is_admitted"] = true_core.is_core_model()
    tests["positive_defined_zero_is_statused"] = true_core.status("p", x) == "defined-zero"
    tests["positive_primitives_preserved_in_completion"] = (
        true_core.completion()["records"][0]["value"] == 0
    )
    tests["wrong_applicability_member_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",), {"p": {("ghost",)}},
        {("p", "d"): set()}, {"p": {}}).is_core_model()
    tests["wrong_prerequisite_member_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",), {"p": set()},
        {("p", "d"): {("ghost",)}}, {"p": {}}).is_core_model()
    tests["wrong_input_arity_in_applicability_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",), {"p": {("x","extra")}},
        {("p", "d"): set()}, {"p": {}}).is_core_model()
    tests["missing_declared_applicability_coordinate_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",), {},
        {("p", "d"): {x}}, {"p": {}}).is_core_model()
    tests["missing_declared_prerequisite_coordinate_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",), {"p": {x}},
        {}, {"p": {}}).is_core_model()
    unavailable = pa.PropertyModel(
        sig, {}, ("p",), {}, {},
        {"p": {("ghost",): 3}})
    supplied_empty = pa.PropertyModel(sig, {"u": ()}, ("p",), {}, {}, {})
    tests["unavailable_and_supplied_empty_are_distinct_at_kind_level"] = (
        not unavailable.profile_available("p") and supplied_empty.profile_available("p")
        and unavailable.status("p") == "profile-unavailable"
    )
    tests["unavailable_and_supplied_empty_input_product_both_return_empty"] = (
        unavailable.input_product("p") == supplied_empty.input_product("p") == set()
    )
    tests["declared_unavailable_surplus_assignment_accepted"] = (
        unavailable.is_core_model() and bool(unavailable.assignments.get("p"))
    )
    tests["undeclared_surplus_relation_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, (), {"p": {x}},
        {("p", "d"): {x}}, {"p": {x: 2}}).is_core_model()
    tests["undeclared_extra_aux_sort_accepted"] = pa.PropertyModel(
        sig, {"rogue": ("z",)}, (), {}, {}, {}).is_core_model()
    tests["value_carrier_not_represented_by_PropertySpec"] = (
        not hasattr(pa.PropertySpec, "value_carrier")
        and pa.PropertySpec.__dataclass_fields__.keys() == {"profile","prerequisites","zero","zero_bearing"}
    )
    arbitrary_value = object()
    tests["unconstrained_assigned_python_value_accepted"] = pa.PropertyModel(
        sig, {"u": ("x",)}, ("p",), {"p": {x}},
        {("p","d"): {x}}, {"p": {x: arbitrary_value}}).is_core_model()
    empty_profile_sig = {"p": pa.PropertySpec(())}
    empty_profile_model = pa.PropertyModel(empty_profile_sig, {}, ("p",), {}, {}, {})
    tests["empty_signature_profile_accepted_despite_m_ge_1"] = (
        empty_profile_model.profile_available("p")
        and empty_profile_model.input_product("p") == {()}
        and empty_profile_model.is_core_model()
    )
    inherited_profile = pa.PropertyModel(
        {"p": pa.PropertySpec(("inherited_h",))}, {}, ("p",), {}, {}, {})
    tests["no_shared_inherited_carrier_interface"] = (
        not inherited_profile.profile_available("p") and
        inherited_profile.status("p") == "profile-unavailable"
    )
    duplicate_model = pa.PropertyModel(
        {"p": pa.PropertySpec(("u",))},
        {"u": ("x", "x")}, (), {}, {}, {})
    single_model = pa.PropertyModel(
        {"p": pa.PropertySpec(("u",))},
        {"u": ("x",)}, (), {}, {}, {})
    tests["duplicate_aux_carrier_tuple_accepted_as_presentation"] = (
        duplicate_model.is_core_model() and
        duplicate_model.input_product("p") == single_model.input_product("p") and
        not pa.carrier_bijection_families(duplicate_model, single_model)
    )
    double_declared=pa.PropertyModel(
        {"p": pa.PropertySpec(("u",))}, {"u": ("x",)}, ("p","p"),
        {"p": {x}}, {}, {"p": {}})
    tests["duplicate_property_declaration_counted_twice"] = (
        double_declared.is_core_model() and
        pa.simple_summary(double_declared)["declared_property_count"] == 2
    )
    invalid_decl=pa.PropertyModel(
        {"p": pa.PropertySpec(("u",))}, {"u": ("x",)}, ("unknown",), {}, {}, {})
    try:
        invalid_decl.is_core_model()
        raises=False
    except KeyError:
        raises=True
    tests["unknown_declaration_raises_not_boolean_validation_result"] = raises
    cm1=pa.construct_pi_countermodel()
    cm2=pa.construct_pii_countermodel()
    tests["C1_completion_runs_on_non_core_PI_counterpremodel"] = (
        not cm1.is_core_model() and
        cm1.status("p",x)=="inapplicable" and
        len(cm1.completion()["records"])==1
    )
    tests["C1_completion_runs_on_non_core_PII_counterpremodel"] = (
        not cm2.is_core_model() and
        cm2.status("p",x)=="prerequisite-unsatisfied" and
        len(cm2.completion()["records"])==1
    )
    witness["core_validity_scope"] = "PI and PII only; assumes well-typed primitive coordinate sets"
    witness["unavailable_distinction"] = (
        "profile_available/status distinguish missing carrier, but input_product returns empty set for both"
    )
    witness["value_type_scope"] = "PropertySpec lacks mathematical value carrier Z_L,pi and so cannot reject outside-codomain values"
    witness["premodel_completion_scope"] = (
        "completion() is callable on PI/PII-violating premodels and yields records; source C1 only claims a full model for admitted primitive cores"
    )
    assert all(tests.values()),{k:v for k,v in tests.items() if not v}
    return {
        "case":"PA-P16-20260901-TYPED-PREMODEL-VALIDATION-AND-C1-INTERFACE-001",
        "source_pdf_sha256":SHA,
        "original_source_files_modified":False,
        "original_test_results_modified":False,
        "number_of_checks":len(tests),
        "passed_expected_negative_and_positive_controls":all(tests.values()),
        "checks":tests,
        "witness_interpretations":witness,
        "not_a_general_typed_validation_proof":True,
        "not_a_general_axiom_refutation":True,
        "original_property_PDF_tex_Zenodo_modified":False,
        "whole_property_FPA":"OPEN"
    }

if __name__=="__main__":
    result=audit()
    txt=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+"\n"
    if len(sys.argv)>1:
        p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(txt,encoding="utf-8")
    print(txt)
    print(f"P16 SOURCE-VS-CODE TYPED AUDIT EXPECTED-DETECTION PASS {result['number_of_checks']} CASES")
