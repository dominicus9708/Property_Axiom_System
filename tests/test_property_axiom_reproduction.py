from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import property_axiom_reproduction as par


class PropertyAxiomReproductionTests(unittest.TestCase):
    def test_primitive_independence_countermodels(self):
        pi = par.construct_pi_countermodel()
        pii = par.construct_pii_countermodel()
        self.assertFalse(pi.primitive_axiom_i())
        self.assertTrue(pi.primitive_axiom_ii())
        self.assertTrue(pii.primitive_axiom_i())
        self.assertFalse(pii.primitive_axiom_ii())

    def test_nontrivial_model_and_completion(self):
        model = par.construct_one_input_model()
        self.assertTrue(model.is_core_model())
        completion = model.completion()
        self.assertEqual(len(completion["records"]), 1)
        self.assertEqual(completion["statuses"]["p"]["('x',)"], "defined-nonzero")

    def test_status_separation(self):
        model = par.construct_status_witness()
        observed = {x[0]: model.status("p", x) for x in sorted(model.input_product("p"))}
        self.assertEqual(observed, par.EXPECTED["statuses"])

    def test_first_branch_witnesses(self):
        for expected, constructor in ((2, par.construct_stage2_branch), (3, par.construct_stage3_branch), (4, par.construct_stage4_branch)):
            a, b = constructor()
            self.assertEqual(par.first_branch(a, b), expected)
            self.assertEqual(len(par.stage_comparison_families(a, b, 4)), len(par.stage_comparison_families(a, b, 5)))

    def test_compression_collision(self):
        a, b = par.construct_stage4_branch()
        self.assertEqual(par.simple_summary(a), par.simple_summary(b))
        self.assertFalse(par.strict_core_isomorphic(a, b))

    def test_forward_map_composition(self):
        a, b, c, f, g = par.construct_forward_map_chain()
        gf = par.compose_carrier_maps(f, g)
        self.assertTrue(par.is_forward_map(a, b, f))
        self.assertTrue(par.is_forward_map(b, c, g))
        self.assertTrue(par.is_forward_map(a, c, gf))

    def test_full_audit(self):
        summary = par.build_summary()
        audit = par.build_audit(summary)
        self.assertTrue(audit["all_checks_pass"], [k for k, v in audit["checks"].items() if not v])


if __name__ == "__main__":
    unittest.main()
