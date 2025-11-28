from django.test import TestCase
from unittest.mock import Mock
import genetics_manager.calculator_utils as utils  # Adjust import path


class CalculatorUtilsTests(TestCase):

    def setUp(self):
        self.recipes = [
            {
                "name": 'Premnas biaculeatus "White Stripe"',
                "criteria": lambda d: d.get("species") == "Premnas biaculeatus",
            },
            {
                "name": "Amphiprion ocellaris",
                "criteria": lambda d: d.get("species") == "Amphiprion ocellaris",
            },
        ]
        self.all_trait_names = []

    def test_premnas_matches_only_premnas(self):
        results = [{"species": "Premnas biaculeatus"}]
        result = utils.analyze_results_by_recipe(
            results, 1, self.recipes, self.all_trait_names
        )
        self.assertEqual(result['Premnas biaculeatus "White Stripe"'], 100.0)

    def test_mixed_species(self):
        results = [
            {"species": "Premnas biaculeatus"},
            {"species": "Amphiprion ocellaris"},
        ]
        result = utils.analyze_results_by_recipe(
            results, 2, self.recipes, self.all_trait_names
        )
        self.assertEqual(result['Premnas biaculeatus "White Stripe"'], 50.0)
        self.assertEqual(result["Amphiprion ocellaris"], 50.0)

    def test_all_non_premnas(self):
        results = [{"species": "Amphiprion ocellaris"}]
        result = utils.analyze_results_by_recipe(
            results, 1, self.recipes, self.all_trait_names
        )
        self.assertEqual(result["Amphiprion ocellaris"], 100.0)
        self.assertNotIn('Premnas biaculeatus "White Stripe"', result)

    # Add this test to catch the real problem
    def test_real_simulation_results(self):
        # Run your actual simulation with known inputs
        from genetics_manager.calculator_utils import (
            generate_results,
        )  # Your sim function

        results = generate_results(
            parent1_genotype, parent2_genotype
        )  # Your real inputs

        print("REAL results species:", [r.get("species") for r in results])
        print("First result keys:", results[0].keys() if results else "NO RESULTS")

        output = utils.analyze_results_by_recipe(
            results, len(results), self.recipes, []
        )
        print("REAL analysis output:", output)

    def test_premnas_criteria_real_data(self):
        premnas_recipe = CommercialPhenotypeRecipe.objects.get(
            name__icontains="Premnas"
        )
        sample_result = {"species": "Amphiprion ocellaris"}  # Non-Premnas

        # This should be FALSE but might be TRUE (your bug!)
        matches_premnas = premnas_recipe.criteria(sample_result)
        self.assertFalse(matches_premnas, "Premnas criteria matches non-Premnas!")
