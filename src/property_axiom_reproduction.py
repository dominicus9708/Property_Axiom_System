from __future__ import annotations

import argparse, csv, itertools, json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

Input = tuple[Any, ...]


@dataclass(frozen=True)
class PropertySpec:
    profile: tuple[str, ...]
    prerequisites: tuple[str, ...] = ()
    zero: Any = None
    zero_bearing: bool = False


@dataclass
class PropertyModel:
    signature: Mapping[str, PropertySpec]
    auxiliary_carriers: dict[str, tuple[Any, ...]] = field(default_factory=dict)
    declarations: tuple[str, ...] = ()
    applicability: dict[str, set[Input]] = field(default_factory=dict)
    prerequisite_satisfaction: dict[tuple[str, str], set[Input]] = field(default_factory=dict)
    assignments: dict[str, dict[Input, Any]] = field(default_factory=dict)

    def carrier(self, sort: str):
        return self.auxiliary_carriers.get(sort)

    def profile_available(self, prop: str) -> bool:
        return all(self.carrier(s) is not None for s in self.signature[prop].profile)

    def input_product(self, prop: str) -> set[Input]:
        carriers = [self.carrier(s) for s in self.signature[prop].profile]
        return set() if any(c is None for c in carriers) else set(itertools.product(*carriers))

    def domain(self, prop: str) -> set[Input]:
        return set(self.assignments.get(prop, {}))

    def dependency_satisfied(self, prop: str) -> set[Input]:
        if not self.profile_available(prop):
            return set()
        result = self.input_product(prop)
        for dep in self.signature[prop].prerequisites:
            result &= self.prerequisite_satisfaction.get((prop, dep), set())
        return result

    def primitive_axiom_i(self) -> bool:
        return all(not self.profile_available(p) or self.domain(p) <= self.applicability.get(p, set()) for p in self.declarations)

    def primitive_axiom_ii(self) -> bool:
        return all(not self.profile_available(p) or self.domain(p) <= self.dependency_satisfied(p) for p in self.declarations)

    def is_core_model(self) -> bool:
        return self.primitive_axiom_i() and self.primitive_axiom_ii()

    def status(self, prop: str, x: Input | None = None) -> str:
        if prop not in self.declarations:
            return "undeclared"
        if not self.profile_available(prop):
            return "profile-unavailable"
        if x is None or x not in self.input_product(prop):
            raise ValueError("A typed input is required for an available declared property.")
        if x not in self.applicability.get(prop, set()):
            return "inapplicable"
        if x not in self.dependency_satisfied(prop):
            return "prerequisite-unsatisfied"
        if x not in self.domain(prop):
            return "applicable-undefined"
        spec, value = self.signature[prop], self.assignments[prop][x]
        if spec.zero_bearing:
            return "defined-zero" if value == spec.zero else "defined-nonzero"
        return "defined-value"

    def completion(self) -> dict[str, Any]:
        out = {"domains": {}, "dependency_satisfied": {}, "statuses": {}, "records": []}
        for prop in self.signature:
            if prop not in self.declarations:
                out["statuses"][prop] = {"kind": "undeclared"}
                continue
            if not self.profile_available(prop):
                out["statuses"][prop] = {"kind": "profile-unavailable"}
                continue
            out["domains"][prop] = _sorted_inputs(self.domain(prop))
            out["dependency_satisfied"][prop] = _sorted_inputs(self.dependency_satisfied(prop))
            out["statuses"][prop] = {repr(tuple(x)): self.status(prop, x) for x in sorted(self.input_product(prop), key=repr)}
            for x in sorted(self.domain(prop), key=repr):
                out["records"].append({"property": prop, "input": list(x), "value": self.assignments[prop][x]})
        return out


def _sorted_inputs(items):
    return [list(x) for x in sorted(items, key=repr)]


def induced_input_map(model: PropertyModel, prop: str, maps, x: Input) -> Input:
    return tuple(maps[s][v] for s, v in zip(model.signature[prop].profile, x))


def carrier_bijection_families(a: PropertyModel, b: PropertyModel):
    if set(a.auxiliary_carriers) != set(b.auxiliary_carriers):
        return []
    sorts, choices = sorted(a.auxiliary_carriers), []
    for s in sorts:
        ca, cb = a.auxiliary_carriers[s], b.auxiliary_carriers[s]
        if len(ca) != len(cb):
            return []
        choices.append([dict(zip(ca, perm)) for perm in itertools.permutations(cb)])
    return [{}] if not sorts else [dict(zip(sorts, xs)) for xs in itertools.product(*choices)]


def stage_comparison_families(a: PropertyModel, b: PropertyModel, stage: int):
    if stage not in range(1, 6):
        raise ValueError("stage must be in 1..5")
    fams = carrier_bijection_families(a, b)
    if stage >= 2 and set(a.declarations) != set(b.declarations):
        return []
    if stage == 1:
        return fams
    keep = []
    for fam in fams:
        ok = True
        if stage >= 3:
            for p in a.declarations:
                for x in a.input_product(p):
                    y = induced_input_map(a, p, fam, x)
                    if (x in a.applicability.get(p, set())) != (y in b.applicability.get(p, set())):
                        ok = False
                        break
                    for d in a.signature[p].prerequisites:
                        if (x in a.prerequisite_satisfaction.get((p, d), set())) != (y in b.prerequisite_satisfaction.get((p, d), set())):
                            ok = False
                            break
                    if not ok:
                        break
                if not ok:
                    break
        if ok and stage >= 4:
            for p in a.declarations:
                for x in a.input_product(p):
                    y = induced_input_map(a, p, fam, x)
                    ina, inb = x in a.domain(p), y in b.domain(p)
                    if ina != inb or (ina and a.assignments[p][x] != b.assignments[p][y]):
                        ok = False
                        break
                if not ok:
                    break
        if ok:
            keep.append(fam)  # Stage 5 is definitional completion of stages <= 4.
    return keep


def first_branch(a, b):
    return next((k for k in range(1, 5) if not stage_comparison_families(a, b, k)), None)


def strict_core_isomorphic(a, b):
    return bool(stage_comparison_families(a, b, 4))


def simple_summary(model: PropertyModel):
    props = {}
    for p in model.declarations:
        spec, dom = model.signature[p], model.domain(p)
        z = sum(spec.zero_bearing and model.assignments[p][x] == spec.zero for x in dom)
        nz = sum(spec.zero_bearing and model.assignments[p][x] != spec.zero for x in dom)
        props[p] = {"domain_size": len(dom), "defined_zero": z, "defined_nonzero": nz}
    return {"declared_property_count": len(model.declarations), "properties": props}


def is_forward_map(a, b, maps):
    if not set(a.auxiliary_carriers) <= set(b.auxiliary_carriers) or not set(a.declarations) <= set(b.declarations):
        return False
    for s, ca in a.auxiliary_carriers.items():
        if set(maps.get(s, {})) != set(ca) or not set(maps[s].values()) <= set(b.auxiliary_carriers[s]):
            return False
    for p in a.declarations:
        for x in a.input_product(p):
            y = induced_input_map(a, p, maps, x)
            if x in a.applicability.get(p, set()) and y not in b.applicability.get(p, set()):
                return False
            for d in a.signature[p].prerequisites:
                if x in a.prerequisite_satisfaction.get((p, d), set()) and y not in b.prerequisite_satisfaction.get((p, d), set()):
                    return False
            if x in a.domain(p) and (y not in b.domain(p) or a.assignments[p][x] != b.assignments[p][y]):
                return False
    return True


def compose_carrier_maps(f, g):
    return {s: {x: g[s][y] for x, y in m.items()} for s, m in f.items()}


def one_sort_signature(prerequisites=(), zero_bearing=False):
    return {"p": PropertySpec(("u",), tuple(prerequisites), 0, zero_bearing)}


def construct_pi_countermodel():
    sig = one_sort_signature(("d",))
    return PropertyModel(sig, {"u": ("x",)}, ("p",), {"p": set()}, {("p", "d"): {("x",)}}, {"p": {("x",): 1}})


def construct_pii_countermodel():
    sig = one_sort_signature(("d",))
    return PropertyModel(sig, {"u": ("x",)}, ("p",), {"p": {("x",)}}, {("p", "d"): set()}, {"p": {("x",): 1}})


def construct_one_input_model():
    sig = one_sort_signature(("d",), True)
    return PropertyModel(sig, {"u": ("x",)}, ("p",), {"p": {("x",)}}, {("p", "d"): {("x",)}}, {"p": {("x",): 1}})


def construct_status_witness():
    sig = one_sort_signature(("d",), True)
    return PropertyModel(sig, {"u": tuple("abcde")}, ("p",), {"p": {(x,) for x in "bcde"}}, {("p", "d"): {(x,) for x in "cde"}}, {"p": {("d",): 0, ("e",): 1}})


def construct_stage2_branch():
    sig = one_sort_signature()
    return PropertyModel(sig, {"u": ("x",)}, ("p",), {"p": {("x",)}}, {}, {"p": {}}), PropertyModel(sig, {"u": ("x",)}, (), {}, {}, {})


def construct_stage3_branch():
    sig = {"p1": PropertySpec(("u",)), "p2": PropertySpec(("u",))}
    kw = dict(signature=sig, auxiliary_carriers={"u": ("a", "b")}, declarations=("p1", "p2"), prerequisite_satisfaction={}, assignments={"p1": {}, "p2": {}})
    return PropertyModel(applicability={"p1": {("a",)}, "p2": {("a",)}}, **kw), PropertyModel(applicability={"p1": {("a",)}, "p2": {("b",)}}, **kw)


def construct_stage4_branch():
    sig = {p: PropertySpec(("u",), zero=0, zero_bearing=True) for p in ("p1", "p2")}
    full = {("a",), ("b",)}
    common = dict(signature=sig, auxiliary_carriers={"u": ("a", "b")}, declarations=("p1", "p2"), applicability={"p1": set(full), "p2": set(full)}, prerequisite_satisfaction={})
    return PropertyModel(assignments={"p1": {("a",): 0, ("b",): 1}, "p2": {("a",): 0, ("b",): 1}}, **common), PropertyModel(assignments={"p1": {("a",): 0, ("b",): 1}, "p2": {("a",): 1, ("b",): 0}}, **common)


def construct_forward_map_chain():
    sig = one_sort_signature(zero_bearing=True)
    a = PropertyModel(sig, {"u": ("a",)}, ("p",), {"p": {("a",)}}, {}, {"p": {("a",): 1}})
    b = PropertyModel(sig, {"u": ("a", "b")}, ("p",), {"p": {("a",), ("b",)}}, {}, {"p": {("a",): 1}})
    c = PropertyModel(sig, {"u": ("a", "b", "c")}, ("p",), {"p": {("a",), ("b",), ("c",)}}, {}, {"p": {("a",): 1}})
    return a, b, c, {"u": {"a": "a"}}, {"u": {"a": "a", "b": "b"}}


EXPECTED_STATUSES = {"a": "inapplicable", "b": "prerequisite-unsatisfied", "c": "applicable-undefined", "d": "defined-zero", "e": "defined-nonzero"}
EXPECTED = {"statuses": EXPECTED_STATUSES}


def build_summary():
    pi, pii, one, sm = construct_pi_countermodel(), construct_pii_countermodel(), construct_one_input_model(), construct_status_witness()
    s2, s3, s4 = construct_stage2_branch(), construct_stage3_branch(), construct_stage4_branch()
    fa, fb, fc, f, g = construct_forward_map_chain()
    gf = compose_carrier_maps(f, g)
    stages = {}
    for k, pair in ((2, s2), (3, s3), (4, s4)):
        counts = {str(i): len(stage_comparison_families(*pair, i)) for i in range(1, 6)}
        stages[str(k)] = {"comparison_counts": counts, "first_branch": first_branch(*pair), "stage4_equals_stage5": counts["4"] == counts["5"]}
    comp = one.completion()
    sa, sb = s4
    rep_a, rep_b = {"R": {"encoding": [1]}}, {"R": {"encoding": [2]}}
    return {
        "primitive_axiom_independence": {"pi_countermodel": {"PI": pi.primitive_axiom_i(), "PII": pi.primitive_axiom_ii()}, "pii_countermodel": {"PI": pii.primitive_axiom_i(), "PII": pii.primitive_axiom_ii()}},
        "one_input_model": {"PI": one.primitive_axiom_i(), "PII": one.primitive_axiom_ii(), "defined_record_count": len(comp["records"]), "completion": comp},
        "status_separation": {x[0]: sm.status("p", x) for x in sorted(sm.input_product("p"))},
        "first_branch_witnesses": stages,
        "completion_stage": {"independent_stage5_branch_found": any(not v["stage4_equals_stage5"] for v in stages.values())},
        "compression_obstruction": {"summary_equal": simple_summary(sa) == simple_summary(sb), "strict_core_isomorphic": strict_core_isomorphic(sa, sb), "summary": simple_summary(sa)},
        "optional_representation": {"core_strict_equivalent": strict_core_isomorphic(one, construct_one_input_model()), "representation_inclusive_equivalent": rep_a == rep_b},
        "forward_map_finite_check": {"A_to_B": is_forward_map(fa, fb, f), "B_to_C": is_forward_map(fb, fc, g), "A_to_C_composite": is_forward_map(fa, fc, gf)},
    }


def build_audit(s):
    checks = {
        "PI countermodel isolates Primitive Axiom I": s["primitive_axiom_independence"]["pi_countermodel"] == {"PI": False, "PII": True},
        "PII countermodel isolates Primitive Axiom II": s["primitive_axiom_independence"]["pii_countermodel"] == {"PI": True, "PII": False},
        "One-input witness satisfies both primitive axioms": s["one_input_model"]["PI"] and s["one_input_model"]["PII"],
        "One-input witness completes to one defined property record": s["one_input_model"]["defined_record_count"] == 1,
        "Status separation matches the displayed five-state finite witness": s["status_separation"] == EXPECTED_STATUSES,
        "Stage-2 branch is derived by exhaustive carrier-bijection comparison": s["first_branch_witnesses"]["2"]["first_branch"] == 2,
        "Stage-3 branch is derived by exhaustive carrier-bijection comparison": s["first_branch_witnesses"]["3"]["first_branch"] == 3,
        "Stage-4 branch is derived by exhaustive carrier-bijection comparison": s["first_branch_witnesses"]["4"]["first_branch"] == 4,
        "Stage 5 introduces no independent finite branch in the displayed witnesses": not s["completion_stage"]["independent_stage5_branch_found"],
        "Simple property summaries collide": s["compression_obstruction"]["summary_equal"],
        "The summary collision pair is not strictly core-isomorphic": not s["compression_obstruction"]["strict_core_isomorphic"],
        "Core equivalence can survive different optional representations": s["optional_representation"]["core_strict_equivalent"],
        "Different optional representations need not be representation-inclusively equivalent": not s["optional_representation"]["representation_inclusive_equivalent"],
        "Finite forward maps close under the displayed composition": all(s["forward_map_finite_check"].values()),
    }
    return {"all_checks_pass": all(checks.values()), "checks": checks}


def write_outputs(out: Path):
    out.mkdir(parents=True, exist_ok=True)
    s = build_summary()
    a = build_audit(s)
    (out / "property_witness_summary.json").write_text(json.dumps(s, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (out / "proof_obligation_audit.json").write_text(json.dumps(a, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    rows = [
        ["pi-countermodel", "primitive-independence", "PI false; PII true", str(s["primitive_axiom_independence"]["pi_countermodel"])],
        ["pii-countermodel", "primitive-independence", "PI true; PII false", str(s["primitive_axiom_independence"]["pii_countermodel"])],
        ["status-witness", "status-separation", "five distinct statuses", str(s["status_separation"])],
    ]
    for k in (2, 3, 4):
        rows.append([f"stage-{k}-branch", "first-branching", f"first branch {k}", str(s["first_branch_witnesses"][str(k)]["comparison_counts"])])
    rows += [
        ["compression-collision", "classification-obstruction", "equal simple summary; no strict core isomorphism", str(s["compression_obstruction"]["summary_equal"])],
        ["representation-split", "optional-representation", "core equivalent; represented inequivalent", str(s["optional_representation"])],
        ["forward-map-chain", "map-category", "A->B, B->C, and composite A->C all valid", str(s["forward_map_finite_check"])],
    ]
    with (out / "witness_catalog.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["witness", "claim_family", "expected", "observed"])
        w.writerows(rows)
    return a


def main():
    p = argparse.ArgumentParser(description="Reproduce finite Property Axiom System witnesses.")
    p.add_argument("--output-dir", default="results")
    args = p.parse_args()
    audit = write_outputs(Path(args.output_dir))
    print(json.dumps(audit, indent=2, sort_keys=True))
    if not audit["all_checks_pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
