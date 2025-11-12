from django.db import models  # Import models for Q objects
from django.shortcuts import get_object_or_404, render

from genetics_manager.calculator_utils import (
    analyze_results_by_recipe,
    cross_fish_structured,
    fish,
)
from genetics_manager.models import CommercialPhenotypeRecipe


def index(request):
    return render(request, "landing/index.html")


def landing_page(request):
    all_clownfish = CommercialPhenotypeRecipe.objects.all().order_by(
        "genus", "species", "variant"
    )
    wild_types = []
    designer_fish = []
    for fish_recipe in all_clownfish:
        is_pure_wild_type = all(
            gene_pair == "+/+" for gene_pair in fish_recipe.genotype.split()
        )
        if is_pure_wild_type:
            wild_types.append(fish_recipe)
        else:
            designer_fish.append(fish_recipe)

    context = {
        "wild_types": wild_types,
        "designer_fish": designer_fish,
    }
    return render(request, "landing/landing.html", context)


def get_phenotype_recipes_from_db():
    formatted_recipes = []
    for db_recipe in CommercialPhenotypeRecipe.objects.all():
        criteria_data = db_recipe.required_genotypes

        def criteria_function(genotype_dict, requirements=criteria_data):
            for locus_name, required_genotype in requirements.items():
                if genotype_dict.get(locus_name) != required_genotype:
                    return False
            return True

        formatted_recipes.append(
            {"name": db_recipe.name, "criteria": criteria_function}
        )
    formatted_recipes.append(
        {"name": "Generic/Unnamed Hybrid", "criteria": lambda g: True}
    )
    return formatted_recipes


def calculate_cross_htmx(request):
    if request.htmx:
        parent1_id = request.session.get("p1_id")
        parent2_id = request.session.get("p2_id")

        if not parent1_id or not parent2_id:
            return render(
                request,
                "landing/partials/error_partial.html",
                {"error_message": "Please select two parents."},
            )

        p1_recipe = get_object_or_404(CommercialPhenotypeRecipe, id=parent1_id)
        p2_recipe = get_object_or_404(CommercialPhenotypeRecipe, id=parent2_id)

        p1_genotypes = p1_recipe.required_genotypes
        p2_genotypes = p2_recipe.required_genotypes

        parent1_fish_obj = fish(p1_genotypes)
        parent2_fish_obj = fish(p2_genotypes)

        results_list, total_count, all_trait_names = cross_fish_structured(
            parent1_fish_obj, parent2_fish_obj
        )

        PHENOTYPE_RECIPES_DB = get_phenotype_recipes_from_db()

        results_percentages = analyze_results_by_recipe(
            results_list, total_count, PHENOTYPE_RECIPES_DB, all_trait_names
        )

        context = {
            "parent1_name": p1_recipe.name,
            "parent2_name": p2_recipe.name,
            "results": results_percentages,
        }
        return render(request, "landing/partials/results_partial.html", context)

    return render(request, "landing/error_page.html")


def select_parent_htmx(request, parent_id):
    parent = get_object_or_404(CommercialPhenotypeRecipe, id=parent_id)
    p1_id = request.session.get("p1_id")
    p2_id = request.session.get("p2_id")

    if not p1_id:
        request.session["p1_id"] = parent.id
        request.session["p1_name"] = parent.name
    elif not p2_id:
        request.session["p2_id"] = parent.id
        request.session["p2_name"] = parent.name
    else:
        request.session["p1_id"] = parent.id
        request.session["p1_name"] = parent.name
        request.session["p2_id"] = None
        request.session["p2_name"] = None

    request.session.modified = True

    context = {
        "p1_name": request.session.get("p1_name", "None"),
        "p2_name": request.session.get("p2_name", "None"),
        "p1_id": request.session.get("p1_id", ""),
        "p2_id": request.session.get("p2_id", ""),
    }
    return render(request, "landing/partials/selection_bar_partial.html", context)


def filter_fish_htmx(request):
    search_query = request.GET.get("search", "").strip()
    filtered_fish = CommercialPhenotypeRecipe.objects.all().order_by(
        "genus", "species", "variant"
    )

    if search_query:
        filtered_fish = filtered_fish.filter(
            models.Q(name__icontains=search_query)
            | models.Q(phenotype__icontains=search_query)
            | models.Q(variant__icontains=search_query)
        )

    wild_types = []
    designer_fish = []
    for fish_recipe in filtered_fish:
        is_pure_wild_type = all(
            gene_pair == "+/+" for gene_pair in fish_recipe.genotype.split()
        )
        if is_pure_wild_type:
            wild_types.append(fish_recipe)
        else:
            designer_fish.append(fish_recipe)

    context = {
        "wild_types": wild_types,
        "designer_fish": designer_fish,
    }
    return render(request, "landing/partials/fish_cards_partial.html", context)
