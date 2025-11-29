import unittest

from genetics_manager.calculator_utils import cross_fish_structured, fish


class TestGeneticsCalculator(unittest.TestCase):
    def test_gold_nugget_goldflake_cross(self):
        """Gold Nugget G/G x Goldflake G/+ → 50% G/G, 50% G/+"""
        # Gold Nugget G/G
        f1 = fish({"Goldflake": "G/G"})
        # Goldflake G/+
        f2 = fish({"Goldflake": "G/+"})

        results_list, total, traits = cross_fish_structured(f1, f2)

        progeny_keys = [r["PROGENY_KEY"] for r in results_list]
        self.assertEqual(sorted(progeny_keys), ["G/+", "G/+", "G/G", "G/G"])

    def test_format_allele_dominant_first(self):
        """format_allele always dominant first"""
        from genetics_manager.calculator_utils import format_allele

        self.assertEqual(format_allele("/", "G"), "G/+")
        self.assertEqual(format_allele("G", "/"), "G/+")
        self.assertEqual(format_allele("G", "G"), "G/G")

    def test_cross_at_index_gold_example(self):
        """Verify cross_at_index produces correct G/+ not +/G"""
        from genetics_manager.calculator_utils import cross_at_index

        # Gold Nugget G/G x Goldflake G/+ aligned
        h_axis = [("G", "+")]  # f1_final
        v_axis = [("G", "G")]  # f2_final

        # Should produce G/+ and G/G only
        keys = []
        for x in range(4):
            for y in range(4):
                result = cross_at_index((x, y), 4, h_axis, v_axis)
                keys.append(result)

        self.assertIn("G/+", keys)
        self.assertIn("G/G", keys)
        self.assertNotIn("+/G", keys)


if __name__ == "__main__":
    unittest.main()
