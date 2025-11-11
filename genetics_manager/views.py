# In clownfishgenetics/landing/views.py (or a new view file)
from django.shortcuts import render
from genetics_manager.models import CommercialPhenotypeRecipe
# Import our calculator utility functions
from genetics_manager.calculator_utils import run_full_cross_process


def calculate_cross_view(request):
    """
    A Django view that runs the genetics calculator based on user input.
    """
    # 1. Get user input (example, you'd get this from request.POST)
    # Let's assume you've already filtered to get the parent objects
    parent1_recipe_id = request.GET.get('parent1_id', 1)
    parent2_recipe_id = request.GET.get('parent2_id', 2)

    parent1_recipe = CommercialPhenotypeRecipe.objects.get(id=parent1_recipe_id)
    parent2_recipe = CommercialPhenotypeRecipe.objects.get(id=parent2_recipe_id)

    # 2. Extract the structured genotype data needed by the calculator
    # The calculator expects a dictionary like {"Overbar": "P/+", "Onyx": "O/+"}
    p1_genotypes = parent1_recipe.required_genotypes
    p2_genotypes = parent2_recipe.required_genotypes

    # 3. Run the full calculation and analysis process using the structured data
    # This calls the functions from calculator_utils.py
    results_percentages = run_full_cross_process(p1_genotypes, p2_genotypes)

    # 4. Pass the results to a Django template for display
    context = {
        'parent1_name': parent1_recipe.name,
        'parent2_name': parent2_recipe.name,
        'results': results_percentages,
    }

    return render(request, 'landing/results_template.html', context)
