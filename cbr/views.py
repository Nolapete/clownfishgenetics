from collections import defaultdict
from itertools import product

from django import forms
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CrossForm, ParentForm, ParentSelectionForm, VarietyForm
from .models import (
    Cross,
    GenotypePhenotype,
    Parent,
    Trait,
    Variety,
)

# Import our calculator utility functions
# from .calculator_utils import run_full_cross_process
# from .services import perform_cross_calculation # Assuming a service function exists
# --- Variety Views ---


class VarietyListView(ListView):
    model = Variety
    template_name = "cbr/variety_list.html"
    context_object_name = "varieties"


class VarietyDetailView(DetailView):
    model = Variety
    template_name = "cbr/variety_detail.html"
    context_object_name = "variety"


class VarietyCreateView(CreateView):
    model = Variety
    form_class = VarietyForm
    template_name = "cbr/variety_form.html"
    success_url = reverse_lazy("variety-list")


# --- Parent Views ---


class ParentListView(ListView):
    model = Parent
    template_name = "cbr/parent_list.html"
    context_object_name = "parents"


class ParentDetailView(DetailView):
    model = Parent
    template_name = "cbr/parent_detail.html"
    context_object_name = "parent"


class ParentCreateView(CreateView):
    model = Parent
    form_class = ParentForm
    template_name = "cbr/parent_form.html"
    success_url = reverse_lazy("parent-list")


# --- Cross Views ---


class CrossListView(ListView):
    model = Cross
    template_name = "cbr/cross_list.html"
    context_object_name = "crosses"


class CrossDetailView(DetailView):
    model = Cross
    template_name = "cbr/cross_detail.html"
    context_object_name = "cross"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["progeny"] = self.object.progeny_set.all()
        return context


class CrossCreateView(CreateView):
    model = Cross
    form_class = CrossForm
    template_name = "cbr/cross_form.html"
    success_url = reverse_lazy("cross-list")


# --- Calculation View (Function-Based) ---
def calculate_cross_results(request, cross_id):
    cross = get_object_or_404(Cross, pk=cross_id)
    # This view would typically call a service function to get results
    # results = perform_cross_calculation(cross)
    results = [  # Placeholder results
        {"phenotype": "Picasso", "genotype": "AB", "ratio": "50%"},
        {"phenotype": "Snowflake", "genotype": "AA", "ratio": "50%"},
    ]

    context = {
        "cross": cross,
        "results": results,
    }
    return render(request, "cbr/cross_results.html", context)


# Helper function to dynamically create the form
def create_dynamic_form(traits):
    """
    Creates a dynamic form class based on traits from the database.
    """
    fields = {}
    for trait in traits:
        alleles = trait.alleles.all()
        choices = [(allele.name, allele.display_name) for allele in alleles]
        fields[f"parent1_genotype_{trait.id}"] = forms.ChoiceField(
            label=f"Parent 1 ({trait.name})",
            choices=choices,
            required=False,  # Allow for optional selection
        )
        fields[f"parent2_genotype_{trait.id}"] = forms.ChoiceField(
            label=f"Parent 2 ({trait.name})",
            choices=choices,
            required=False,  # Allow for optional selection
        )
    return type("DynamicGenotypeForm", (forms.Form,), fields)


# Helper function to get phenotype based on traits and alleles
def get_phenotype(
    trait, allele_pair, genotype_phenotype_map, parent1=None, parent2=None
):
    """
    Looks up the phenotype for a given trait and allele pair,
    with optional context from parent fish.
    """
    genotype_key = "".join(sorted(allele_pair))

    phenotype = genotype_phenotype_map.get(trait.id, {}).get(genotype_key)

    # Advanced logic based on parent context (if needed)
    if phenotype is None:
        if parent1 and parent2 and parent1.species != parent2.species:
            phenotype = "Hybrid Offspring"
        else:
            phenotype = "Unknown"

    return phenotype


def calculator_view(request):
    traits = Trait.objects.all()
    DynamicGenotypeForm = create_dynamic_form(traits)
    form = DynamicGenotypeForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            selected_traits = [
                trait
                for trait in traits
                if form.cleaned_data.get(f"parent1_genotype_{trait.id}")
                and form.cleaned_data.get(f"parent2_genotype_{trait.id}")
            ]

            if not selected_traits:
                form_fields = []
                for trait in traits:
                    p1_field_name = f"parent1_genotype_{trait.id}"
                    p2_field_name = f"parent2_genotype_{trait.id}"
                    form_fields.append(
                        {
                            "trait": trait,
                            "p1_field": form[p1_field_name],
                            "p2_field": form[p2_field_name],
                        }
                    )

                context = {
                    "form": form,
                    "form_fields": form_fields,
                    "traits": traits,
                    "error": "Please select at least one trait for both parents.",
                }
                return render(request, "cbr/calculator_input.html", context)

            parent1_alleles_by_trait = {
                trait.id: [form.cleaned_data[f"parent1_genotype_{trait.id}"]]
                for trait in selected_traits
            }
            parent2_alleles_by_trait = {
                trait.id: [form.cleaned_data[f"parent2_genotype_{trait.id}"]]
                for trait in selected_traits
            }

            parent1_alleles_list = [
                parent1_alleles_by_trait[trait.id] for trait in selected_traits
            ]
            parent2_alleles_list = [
                parent2_alleles_by_trait[trait.id] for trait in selected_traits
            ]

            gametes_p1 = ["".join(g) for g in product(*parent1_alleles_list)]
            gametes_p2 = ["".join(g) for g in product(*parent2_alleles_list)]

            genotype_phenotype_map = defaultdict(dict)
            for entry in GenotypePhenotype.objects.filter(trait__in=selected_traits):
                alleles = "".join(sorted([entry.allele1.name, entry.allele2.name]))
                genotype_phenotype_map[entry.trait.id][alleles] = entry.phenotype

            punnett_square = []
            phenotype_counts = defaultdict(int)

            for g1 in gametes_p1:
                row = []
                for g2 in gametes_p2:
                    offspring_alleles = []
                    offspring_phenotype_str = ""

                    for i, trait in enumerate(selected_traits):
                        allele_pair = sorted([g1[i], g2[i]])
                        offspring_alleles.append("".join(allele_pair))

                        phenotype = get_phenotype(
                            trait, allele_pair, genotype_phenotype_map
                        )
                        offspring_phenotype_str += f"{trait.name}: {phenotype}, "

                    offspring_genotype_str = "".join(sorted(offspring_alleles))
                    row.append(
                        {
                            "genotype": offspring_genotype_str,
                            "phenotype": offspring_phenotype_str.strip(", "),
                        }
                    )
                    phenotype_counts[offspring_phenotype_str.strip(", ")] += 1
                punnett_square.append(row)

            total_offspring = sum(phenotype_counts.values())
            phenotype_percentages = {
                pheno: (count / total_offspring) * 100
                for pheno, count in phenotype_counts.items()
            }

            context = {
                "form": form,
                "traits": selected_traits,
                "punnett_square": punnett_square,
                "parent1_gametes": gametes_p1,
                "parent2_gametes": gametes_p2,
                "phenotype_percentages": phenotype_percentages,
            }
            return render(request, "cbr/calculator_result.html", context)
    else:
        form = DynamicGenotypeForm()

    form_fields = []
    for trait in traits:
        p1_field_name = f"parent1_genotype_{trait.id}"
        p2_field_name = f"parent2_genotype_{trait.id}"
        form_fields.append(
            {
                "trait": trait,
                "p1_field": form[p1_field_name],
                "p2_field": form[p2_field_name],
            }
        )

    context = {
        "form": form,
        "form_fields": form_fields,
        "traits": traits,
    }

    return render(request, "cbr/calculator_input.html", context)


def parent_selection_view(request):
    punnett_square = None
    phenotype_percentages = None
    form = ParentSelectionForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        parent1 = form.cleaned_data["parent1"]
        parent2 = form.cleaned_data["parent2"]

        shared_trait_ids = {
            g.trait_id for g in parent1.clownfishgenotype_set.all()
        }.intersection({g.trait_id for g in parent2.clownfishgenotype_set.all()})

        selected_traits = Trait.objects.filter(id__in=shared_trait_ids)

        parent1_alleles_list = [
            [g.allele1.name, g.allele2.name]
            for g in parent1.clownfishgenotype_set.filter(trait__in=selected_traits)
        ]
        parent2_alleles_list = [
            [g.allele1.name, g.allele2.name]
            for g in parent2.clownfishgenotype_set.filter(trait__in=selected_traits)
        ]

        gametes_p1 = ["".join(g) for g in product(*parent1_alleles_list)]
        gametes_p2 = ["".join(g) for g in product(*parent2_alleles_list)]

        genotype_phenotype_map = defaultdict(dict)
        for entry in GenotypePhenotype.objects.filter(trait__in=selected_traits):
            alleles = "".join(sorted([entry.allele1.name, entry.allele2.name]))
            genotype_phenotype_map[entry.trait_id][alleles] = entry.phenotype

        punnett_square = []
        phenotype_counts = defaultdict(int)

        for g1 in gametes_p1:
            row = []
            for g2 in gametes_p2:
                offspring_phenotype_str = ""
                for i, trait in enumerate(selected_traits):
                    allele_pair = sorted([g1[i], g2[i]])
                    phenotype = get_phenotype(
                        trait,
                        allele_pair,
                        genotype_phenotype_map,
                        parent1=parent1,
                        parent2=parent2,
                    )
                    offspring_phenotype_str += f"{trait.name}: {phenotype}, "

                offspring_genotype_str = "".join(
                    sorted(
                        [
                            "".join(sorted([g1[i], g2[i]]))
                            for i in range(len(selected_traits))
                        ]
                    )
                )

                row.append(
                    {
                        "genotype": offspring_genotype_str,
                        "phenotype": offspring_phenotype_str.strip(", "),
                    }
                )
                phenotype_counts[offspring_phenotype_str.strip(", ")] += 1
            punnett_square.append(row)

        total_offspring = sum(phenotype_counts.values())
        if total_offspring > 0:
            phenotype_percentages = {
                pheno: (count / total_offspring) * 100
                for pheno, count in phenotype_counts.items()
            }

        punnett_with_gametes = list(zip(gametes_p1, punnett_square, strict=False))

        context = {
            "form": form,
            "punnett_with_gametes": punnett_with_gametes,
            "parent1_gametes": gametes_p1,
            "parent2_gametes": gametes_p2,
            "phenotype_percentages": phenotype_percentages,
            "parent1": parent1,
            "parent2": parent2,
            "traits": selected_traits,
        }
        return render(request, "cbr/parent_selection_result.html", context)

    context = {"form": form}
    return render(request, "cbr/parent_selection_input.html", context)


# def calculate_cross_view(request):
#     """
#     A Django view that runs the genetics calculator based on user input.
#     """
#     # 1. Get user input (example, you'd get this from request.POST)
#     # Let's assume you've already filtered to get the parent objects
#     parent1_recipe_id = request.GET.get("parent1_id", 1)
#     parent2_recipe_id = request.GET.get("parent2_id", 2)
#
#     parent1_recipe = CommercialPhenotypeRecipe.objects.get(id=parent1_recipe_id)
#     parent2_recipe = CommercialPhenotypeRecipe.objects.get(id=parent2_recipe_id)
#
#     # 2. Extract the structured genotype data needed by the calculator
#     # The calculator expects a dictionary like {"Overbar": "P/+", "Onyx": "O/+"}
#     p1_genotypes = parent1_recipe.required_genotypes
#     p2_genotypes = parent2_recipe.required_genotypes
#
#     # 3. Run the full calculation and analysis process using the structured data
#     # This calls the functions from calculator_utils.py
#     results_percentages = run_full_cross_process(p1_genotypes, p2_genotypes)
#
#     # 4. Pass the results to a Django template for display
#     context = {
#         "parent1_name": parent1_recipe.name,
#         "parent2_name": parent2_recipe.name,
#         "results": results_percentages,
#     }
#
#     return render(request, "landing/results_template.html", context)
