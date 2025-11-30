# Setup Django environment if running standalone (adjust your project name)
# Uncomment below if you run outside manage.py shell
# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
# django.setup()

from django.db import transaction

from genetics_manager.models import CommercialPhenotypeRecipe, Locus


def main():
    loci = list(Locus.objects.order_by("id"))
    print(f"Loci found ({len(loci)}): {[allele.name for allele in loci]}")

    # Filter recipes with empty required_genotypes and genotype != "+/+"
    # Also include recipes with incorrect required_genotypes
    recipes = CommercialPhenotypeRecipe.objects.filter(genotype__ne="+/+")

    updated_count = 0
    incorrect_count = 0
    empty_count = 0

    with transaction.atomic():
        for recipe in recipes:
            genotype_pairs = recipe.genotype.split()
            if len(genotype_pairs) != len(loci):
                print(
                    f"SKIP: {recipe.name} genotype count "
                    f"({len(genotype_pairs)}) != loci count ({len(loci)})"
                )
                continue

            expected = {
                locus.name: pair
                for locus, pair in zip(loci, genotype_pairs, strict=True)
            }
            if (not recipe.required_genotypes or recipe.required_genotypes) == {}:
                # Empty required_genotypes, populate it
                recipe.required_genotypes = expected
                recipe.save(update_fields=["required_genotypes"])
                empty_count += 1
                updated_count += 1
                print(f"POPULATED: {recipe.name}")
            else:
                # Verify correctness
                if recipe.required_genotypes != expected:
                    incorrect_count += 1
                    print(f"INCORRECT: {recipe.name}")
                    print(f" Existing: {recipe.required_genotypes}")
                    print(f" Expected: {expected}")
                    # Uncomment below lines to auto-correct:
                    # recipe.required_genotypes = expected
                    # recipe.save(update_fields=["required_genotypes"])
                    # updated_count += 1
                    # print(f"CORRECTED: {recipe.name}")

    print(
        f"Done. Empty populated: {empty_count}, "
        f"Incorrect detected: {incorrect_count}, "
        f"Total updated: {updated_count}"
    )
