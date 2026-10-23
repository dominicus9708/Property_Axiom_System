#!/usr/bin/env python3
"""Source-locked negative control audit, leaves original src/, tests/, results/ unchanged.

Kwon Dominicus, Property Axiom System general model (paper dated 2026-09-01).
Run at existing repo root:
  python audits/2026-09-01/PA-REPLAY-20261024_NEGATIVE_CONTROLS.py
Only supports *scope/coverage findings*, not a repair or machine proof.
"""
from __future__ import annotations
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
import property_axiom_reproduction as par

PAPER_SHA256 = "03a7e5693b73f0332e71a5eb83483e4f3539fc940d5368d5eec1523867e3d79c"


def audit():
    checked = {}
    spec = {"p": par.PropertySpec(("u",), ())}
    # The source requires Ap to be a subset of the *typed product*. Neither
    # is_core_model nor the two core-axiom methods check typing separately.
    m = par.PropertyModel(
        signature=spec, auxiliary_carriers={"u": ("x",)},
        declarations=("p",), applicability={"p": {("ghost",)}},
        assignments={"p": {}})
    checked["untyped_applicability_accepted_by_is_core_model"] = (
        ("ghost",) not in m.input_product("p") and m.is_core_model())
    spec_dep = {"p": par.PropertySpec(("u",), ("d",))}
    n = par.PropertyModel(
        signature=spec_dep, auxiliary_carriers={"u": ("x",)},
        declarations=("p",), applicability={"p": set()},
        prerequisite_satisfaction={("p", "d"): {("ghost",)}},
        assignments={"p": {}})
    checked["untyped_dependency_set_accepted_by_is_core_model"] = (
        ("ghost",) not in n.input_product("p") and n.is_core_model())
    # The constructor doesn't reject a surplus assignment on a declared
    # profile-unavailable kind; source says no coordinates are required.
    # Whether surplus metadata are forbidden vs ignored is a modeling policy
    # question, NOT a claimed contradiction of the source itself.
    u = par.PropertyModel(signature=spec, auxiliary_carriers={},
                          declarations=("p",),
                          assignments={"p": {("ghost",): 7}})
    checked["unavailable_profile_surplus_assignment_not_rejected"] = (
        not u.profile_available("p") and u.is_core_model()
        and bool(u.assignments["p"]))

    cm1=par.construct_pi_countermodel()
    cm2=par.construct_pii_countermodel()
    x=("x",)
    checked["PI_counterpremodel_has_overlapping_raw_predicates"] = (
        x not in cm1.applicability["p"] and x in cm1.domain("p")
        and cm1.status("p", x)=="inapplicable")
    checked["PII_counterpremodel_has_overlapping_raw_predicates"] = (
        x in cm2.applicability["p"] and
        x not in cm2.dependency_satisfied("p")
        and x in cm2.domain("p")
        and cm2.status("p",x)=="prerequisite-unsatisfied")
    checked["counterpremodels_not_both_axioms_admitted"] = (
        not cm1.is_core_model() and not cm2.is_core_model())

    with tempfile.TemporaryDirectory(prefix="property-replay-audit-") as d:
        out=Path(d)
        par.write_outputs(out)
        verifier=ROOT/"src"/"verify_property_axiom_results.py"
        baseline=subprocess.run([sys.executable,str(verifier),"--results-dir",str(out)],
                               capture_output=True,text=True,timeout=20)
        checked["original_verifier_accepts_fresh_original_outputs"] = baseline.returncode==0
        # Mutation: this verifier checks only a subset of the summary and
        # trusts a single audit all_checks_pass flag. It is NOT an independent
        # recomputation of the full witness or audit JSON.
        p=out/"property_witness_summary.json"
        s=json.loads(p.read_text(encoding="utf-8"))
        s["status_separation"]["a"]="intentionally-corrupted"
        p.write_text(json.dumps(s,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        tamper1=subprocess.run([sys.executable,str(verifier),"--results-dir",str(out)],
                               capture_output=True,text=True,timeout=20)
        checked["original_verifier_misses_corrupted_status_witness"] = tamper1.returncode==0
        audit_path=out/"proof_obligation_audit.json"
        a=json.loads(audit_path.read_text(encoding="utf-8"))
        key=next(iter(a["checks"]))
        a["checks"][key]=False
        a["all_checks_pass"]=True
        audit_path.write_text(json.dumps(a,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        tamper2=subprocess.run([sys.executable,str(verifier),"--results-dir",str(out)],
                               capture_output=True,text=True,timeout=20)
        checked["original_verifier_trusts_all_checks_pass_despite_false_detail"] = tamper2.returncode==0
    assert all(checked.values()), checked
    return {
        "case":"PA-REPLAY-20261024-ORIGINAL-NONDESTRUCTIVE-NEGATIVE-CONTROLS",
        "source_pdf_sha256":PAPER_SHA256,
        "original_code_changed":False,
        "original_results_mutated":False,
        "tests":checked,
        "scope":"original Python is a finite witness generator, not a full typed model validator or independent verifier",
        "mathematical_core_axioms_refuted":False,
        "type_validator_completeness_proven":False,
        "full_property_fpa":"OPEN"
    }

if __name__=="__main__":
    data=audit()
    print(json.dumps(data,ensure_ascii=False,indent=2,sort_keys=True))
    print("PAPER-SOURCE-BOUND NEGATIVE AUDIT EXPECTED-DETECTION PASS",
          len(data["tests"]),"cases")
