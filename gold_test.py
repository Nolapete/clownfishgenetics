from django.db.models import Q

from calcRefactor.models import Cross, Progeny, Variety
from genetics_manager.calculator_utils import cross_fish_structured, fish
from genetics_manager.models import CommercialPhenotypeRecipe

# Use your actual recipe IDs/names from session
p1_recipe = CommercialPhenotypeRecipe.objects.get(name__icontains="Gold Nugget")
p2_recipe = CommercialPhenotypeRecipe.objects.get(name__icontains="Goldflake")
p1 = fish(p1_recipe.required_genotypes)
p2 = fish(p2_recipe.required_genotypes)

results, total, traits = cross_fish_structured(p1, p2)
print("=== GOLD CROSS DEBUG ===")
print("Traits:", traits)
print("Total progeny:", total)
print("PROGENY_KEYS:", [r["PROGENY_KEY"] for r in results])
print("Wildtype count:", len([r for r in results if r["PROGENY_KEY"] == "+/+"]))
print("First 4 results:", results[:4])


gold_nugget = Variety.objects.get(name__icontains="Gold Nugget")
gold_flake = Variety.objects.get(name__icontains="Goldflake")
cross = Cross.objects.filter(
    Q(parent1__variety=gold_nugget, parent2__variety=gold_flake)
    | Q(parent1__variety=gold_flake, parent2__variety=gold_nugget)
).first()
print("Gold Cross ID:", cross.id)


print("Progeny Test")
gold_progeny = Progeny.objects.filter(cross__id=3)  # Your Gold cross ID
print("DB GENOTYPES:", [p.genotype for p in gold_progeny])
