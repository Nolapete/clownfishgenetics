from django.db import models  # Import models for Q objects
from django.shortcuts import get_object_or_404, render

from calcRefactor.models import Cross, Progeny, Variety
from genetics_manager.calculator_utils import (
    cross_fish_structured,
    fish,
)
from genetics_manager.models import CommercialPhenotypeRecipe


def index(request):
    return render(request, "landing/index.html")


def about(request):
    return render(request, "landing/about.html")


def contact(request):
    return render(request, "landing/contact.html")


def privacy_policy(request):
    return render(request, "landing/privacy_policy.html")


def cbr(request):
    return render(
        request,
        "landing/cbr.html",
        {
            "site_name": "Clownfish Genetics",
            "primary_color": "#FF6B35",
            "secondary_color": "#F7931E",
            "hero_image": "images/clownfish-hero.jpg",
        },
    )


def landing_page(request):
    all_clownfish = CommercialPhenotypeRecipe.objects.all().order_by(
        "genus", "species", "variant"
    )
    wild_types = [recipe for recipe in all_clownfish if recipe.is_pure_wild_type]
    designer_fish = [recipe for recipe in all_clownfish if not recipe.is_pure_wild_type]

    context = {"wild_types": wild_types, "designer_fish": designer_fish}
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

        # === ROBUST FALLBACK: NO CROSS DATA ===
        # FIXED: Safe exact match instead of icontains
        try:
            variety1 = Variety.objects.get(name__exact=p1_recipe.name)
        except (Variety.MultipleObjectsReturned, Variety.DoesNotExist):
            variety1 = Variety.objects.filter(name__exact=p1_recipe.name).first()

        try:
            variety2 = Variety.objects.get(name__exact=p2_recipe.name)
        except (Variety.MultipleObjectsReturned, Variety.DoesNotExist):
            variety2 = Variety.objects.filter(name__exact=p2_recipe.name).first()

        cross = Cross.objects.filter(
            models.Q(parent1__variety=variety1, parent2__variety=variety2)
            | models.Q(parent1__variety=variety2, parent2__variety=variety1)
        ).first()

        if not cross:  # NO CROSS OR PROGENY DATA
            if p1_recipe.name == p2_recipe.name:
                # IDENTICAL PARENTS - use legacy genotype field
                p1_geno_str = p1_recipe.genotype or "+/+"
                results = {
                    f"{p1_recipe.name} {p1_geno_str}": {
                        "percentage": 100.0,
                        "genotype": "",
                    }
                }
            else:
                # DIFFERENT PARENTS - use legacy genotype fields
                p1_geno_str = p1_recipe.genotype or "+/+"
                p2_geno_str = p2_recipe.genotype or "+/+"
                results = {
                    f"{p1_recipe.name} {p1_geno_str} "
                    f"x {p2_recipe.name} {p2_geno_str}": {
                        "percentage": 100.0,
                        "genotype": "",
                    }
                }
            context = {
                "parent1_name": p1_recipe.name,
                "parent2_name": p2_recipe.name,
                "results": results,
            }
            return render(request, "landing/partials/results_partial.html", context)
        # === END ROBUST FALLBACK ===

        # WILDTYPE SPECIAL CASE (still needed for identical wildtype)
        if (not p1_genotypes or p1_genotypes == {}) and (
            not p2_genotypes or p2_genotypes == {}
        ):
            if p1_recipe.name == p2_recipe.name:
                results = {
                    f"{p1_recipe.name} +/+": {"percentage": 100.0, "genotype": ""}
                }
            else:
                results = {
                    f"{p1_recipe.name} +/+ x {p2_recipe.name} +/+": {
                        "percentage": 100.0,
                        "genotype": "",
                    }
                }
            context = {
                "parent1_name": p1_recipe.name,
                "parent2_name": p2_recipe.name,
                "results": results,
            }
            return render(request, "landing/partials/results_partial.html", context)

        # NORMAL GENETICS CALCULATION
        parent1_fish_obj = fish(p1_genotypes)
        parent2_fish_obj = fish(p2_genotypes)

        results_list, total_count, all_trait_names = cross_fish_structured(
            parent1_fish_obj, parent2_fish_obj
        )

        # FIXED: Safe exact match (second occurrence)
        try:
            variety1 = Variety.objects.get(name__exact=p1_recipe.name)
        except (Variety.MultipleObjectsReturned, Variety.DoesNotExist):
            variety1 = Variety.objects.filter(name__exact=p1_recipe.name).first()

        try:
            variety2 = Variety.objects.get(name__exact=p2_recipe.name)
        except (Variety.MultipleObjectsReturned, Variety.DoesNotExist):
            variety2 = Variety.objects.filter(name__exact=p2_recipe.name).first()

        cross = Cross.objects.filter(
            models.Q(parent1__variety=variety1, parent2__variety=variety2)
            | models.Q(parent1__variety=variety2, parent2__variety=variety1)
        ).first()

        if cross:
            progeny_map = {
                p.genotype: p.phenotype_name
                for p in Progeny.objects.filter(cross=cross).distinct("genotype")
            }
            print(f"DEBUG - Cross found: {cross}")
            print(f"DEBUG - Progeny map: {progeny_map}")
            print(
                f"DEBUG - results_list PROGENY_KEYs: "
                f"{[offspring.get('PROGENY_KEY') for offspring in results_list]}"
            )
        else:
            print("DEBUG - No cross found")
            progeny_map = {}

        results = {}  # phenotype → {percentage, genotype}

        for offspring in results_list:
            progeny_key = offspring.get("PROGENY_KEY", "+/+")
            if progeny_key in progeny_map:
                phenotype = progeny_map[progeny_key]
                percentage = 100.0 / total_count
                if phenotype not in results:
                    results[phenotype] = {"percentage": 0.0, "genotype": progeny_key}
                results[phenotype]["percentage"] += percentage

        print(f"Final results: {results}")

        context = {
            "parent1_name": p1_recipe.name,
            "parent2_name": p2_recipe.name,
            "results": results,
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

    wild_types = [recipe for recipe in filtered_fish if recipe.is_pure_wild_type]
    designer_fish = [recipe for recipe in filtered_fish if not recipe.is_pure_wild_type]

    context = {"wild_types": wild_types, "designer_fish": designer_fish}
    return render(request, "landing/partials/fish_cards_partial.html", context)
