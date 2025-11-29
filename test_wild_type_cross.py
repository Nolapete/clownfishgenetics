# test_wild_type_cross_debug.py
from genetics_manager.calculator_utils import (
    analyze_results_by_recipe,
    cross_fish_structured,
    fish,
)
from genetics_manager.models import CommercialPhenotypeRecipe, Locus
from landing.views import get_phenotype_recipes_from_db

print("=== DEBUG WILDTYPE ===")

# Wild parents
wild_recipe = CommercialPhenotypeRecipe.objects.filter(
    name__icontains="Amphiprion ocellaris"
).first()
trait_dict = {locus.name: "+/+" for locus in list(Locus.objects.order_by("id"))}

f1 = fish(trait_dict)
results_list, total_count, all_trait_names = cross_fish_structured(f1, f1)

print(f"Wild recipe: {wild_recipe.name}")
print(f"Wild required_genotypes: {wild_recipe.required_genotypes}")
print(f"Sample offspring: {results_list[0]}")

# Test recipes with DEBUG
recipes = get_phenotype_recipes_from_db()  # Your function
print(f"\nRecipes loaded: {[r['name'] for r in recipes]}")

# Test FIRST offspring against ALL recipes
sample = results_list[0]
print(f"\n=== DEBUG: Testing sample {sample} ===")
for recipe in recipes:
    match = recipe["criteria"](sample)
    print(f"  {recipe['name']}: {match}")

results = analyze_results_by_recipe(results_list, total_count, recipes, all_trait_names)
print(f"\nFinal results: {results}")
