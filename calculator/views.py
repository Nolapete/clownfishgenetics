from django import forms
from django.shortcuts import render
from itertools import product
from collections import defaultdict
from .models import Trait, Allele, GenotypePhenotype, Clownfish
from .forms import ParentSelectionForm

# Helper function to dynamically create the form
def create_dynamic_form(traits):
    """
    Creates a dynamic form class based on traits from the database.
    """
    fields = {}
    for trait in traits:
        alleles = trait.alleles.all()
        choices = [(allele.name, allele.display_name) for allele in alleles]
        fields[f'parent1_genotype_{trait.id}'] = forms.ChoiceField(
            label=f'Parent 1 ({trait.name})',
            choices=choices,
            required=False # Allow for optional selection
        )
        fields[f'parent2_genotype_{trait.id}'] = forms.ChoiceField(
            label=f'Parent 2 ({trait.name})',
            choices=choices,
            required=False # Allow for optional selection
        )
    return type('DynamicGenotypeForm', (forms.Form,), fields)

# Helper function to get phenotype based on traits and alleles
def get_phenotype(trait, allele_pair, genotype_phenotype_map, parent1=None, parent2=None):
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
            phenotype = 'Unknown'
    
    return phenotype

def calculator_view(request):
    traits = Trait.objects.all()
    DynamicGenotypeForm = create_dynamic_form(traits)
    form = DynamicGenotypeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            selected_traits = [
                trait for trait in traits
                if form.cleaned_data.get(f'parent1_genotype_{trait.id}') and form.cleaned_data.get(f'parent2_genotype_{trait.id}')
            ]

            if not selected_traits:
                form_fields = []
                for trait in traits:
                    p1_field_name = f"parent1_genotype_{trait.id}"
                    p2_field_name = f"parent2_genotype_{trait.id}"
                    form_fields.append({
                        'trait': trait,
                        'p1_field': form[p1_field_name],
                        'p2_field': form[p2_field_name],
                    })

                context = {
                    'form': form,
                    'form_fields': form_fields,
                    'traits': traits,
                    'error': 'Please select at least one trait for both parents.',
                }
                return render(request, 'calculator/calculator_input.html', context)

            parent1_alleles_by_trait = {
                trait.id: [form.cleaned_data[f'parent1_genotype_{trait.id}']]
                for trait in selected_traits
            }
            parent2_alleles_by_trait = {
                trait.id: [form.cleaned_data[f'parent2_genotype_{trait.id}']]
                for trait in selected_traits
            }

            parent1_alleles_list = [parent1_alleles_by_trait[trait.id] for trait in selected_traits]
            parent2_alleles_list = [parent2_alleles_by_trait[trait.id] for trait in selected_traits]

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

                        phenotype = get_phenotype(trait, allele_pair, genotype_phenotype_map)
                        offspring_phenotype_str += f"{trait.name}: {phenotype}, "

                    offspring_genotype_str = "".join(sorted(offspring_alleles))
                    row.append({'genotype': offspring_genotype_str, 'phenotype': offspring_phenotype_str.strip(', ')})
                    phenotype_counts[offspring_phenotype_str.strip(', ')] += 1
                punnett_square.append(row)

            total_offspring = sum(phenotype_counts.values())
            phenotype_percentages = {
                pheno: (count / total_offspring) * 100
                for pheno, count in phenotype_counts.items()
            }

            context = {
                'form': form,
                'traits': selected_traits,
                'punnett_square': punnett_square,
                'parent1_gametes': gametes_p1,
                'parent2_gametes': gametes_p2,
                'phenotype_percentages': phenotype_percentages,
            }
            return render(request, 'calculator/calculator_result.html', context)
    else:
        form = DynamicGenotypeForm()

    form_fields = []
    for trait in traits:
        p1_field_name = f"parent1_genotype_{trait.id}"
        p2_field_name = f"parent2_genotype_{trait.id}"
        form_fields.append({
            'trait': trait,
            'p1_field': form[p1_field_name],
            'p2_field': form[p2_field_name],
        })

    context = {
        'form': form,
        'form_fields': form_fields,
        'traits': traits,
    }

    return render(request, 'calculator/calculator_input.html', context)


def parent_selection_view(request):
    punnett_square = None
    phenotype_percentages = None
    form = ParentSelectionForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        parent1 = form.cleaned_data['parent1']
        parent2 = form.cleaned_data['parent2']

        shared_trait_ids = {g.trait_id for g in parent1.clownfishgenotype_set.all()}.intersection(
            {g.trait_id for g in parent2.clownfishgenotype_set.all()}
        )
        
        selected_traits = Trait.objects.filter(id__in=shared_trait_ids)

        parent1_alleles_list = [[g.allele1.name, g.allele2.name] for g in parent1.clownfishgenotype_set.filter(trait__in=selected_traits)]
        parent2_alleles_list = [[g.allele1.name, g.allele2.name] for g in parent2.clownfishgenotype_set.filter(trait__in=selected_traits)]
        
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
                    phenotype = get_phenotype(trait, allele_pair, genotype_phenotype_map, parent1=parent1, parent2=parent2)
                    offspring_phenotype_str += f"{trait.name}: {phenotype}, "

                offspring_genotype_str = "".join(sorted(["".join(sorted([g1[i], g2[i]])) for i in range(len(selected_traits))]))

                row.append({'genotype': offspring_genotype_str, 'phenotype': offspring_phenotype_str.strip(', ')})
                phenotype_counts[offspring_phenotype_str.strip(', ')] += 1
            punnett_square.append(row)

        total_offspring = sum(phenotype_counts.values())
        if total_offspring > 0:
            phenotype_percentages = {
                pheno: (count / total_offspring) * 100
                for pheno, count in phenotype_counts.items()
            }

        punnett_with_gametes = list(zip(gametes_p1, punnett_square))

        context = {
            'form': form,
            'punnett_with_gametes': punnett_with_gametes,
            'parent1_gametes': gametes_p1,
            'parent2_gametes': gametes_p2,
            'phenotype_percentages': phenotype_percentages,
            'parent1': parent1,
            'parent2': parent2,
            'traits': selected_traits,
        }
        return render(request, 'calculator/parent_selection_result.html', context)

    context = {'form': form}
    return render(request, 'calculator/parent_selection_input.html', context)
