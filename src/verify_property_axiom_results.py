from __future__ import annotations

import argparse
import json
from pathlib import Path

EXPECTED_FILES = (
    "property_witness_summary.json",
    "proof_obligation_audit.json",
    "witness_catalog.csv",
)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify Property Axiom System reproduction outputs.")
    parser.add_argument("--results-dir", default="results")
    args = parser.parse_args()
    root = Path(args.results_dir)

    missing = [name for name in EXPECTED_FILES if not (root / name).is_file()]
    if missing:
        raise SystemExit(f"Missing deterministic outputs: {', '.join(missing)}")

    audit = json.loads((root / "proof_obligation_audit.json").read_text(encoding="utf-8"))
    if not audit.get("all_checks_pass", False):
        failed = [name for name, ok in audit.get("checks", {}).items() if not ok]
        raise SystemExit("Failed proof-obligation checks: " + "; ".join(failed))

    summary = json.loads((root / "property_witness_summary.json").read_text(encoding="utf-8"))
    branches = summary["first_branch_witnesses"]
    if {k: branches[k]["first_branch"] for k in ("2", "3", "4")} != {"2": 2, "3": 3, "4": 4}:
        raise SystemExit("First-branch regression mismatch.")
    if summary["completion_stage"]["independent_stage5_branch_found"]:
        raise SystemExit("Unexpected independent Stage-5 branch in displayed witnesses.")
    if not summary["compression_obstruction"]["summary_equal"] or summary["compression_obstruction"]["strict_core_isomorphic"]:
        raise SystemExit("Compression-obstruction regression mismatch.")

    print("Property Axiom System deterministic results verified.")


if __name__ == "__main__":
    main()
