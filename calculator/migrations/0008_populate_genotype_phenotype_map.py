# calculator/migrations/0008_populate_genotype_phenotype_map.py

from django.db import migrations, transaction
from django.core.exceptions import ObjectDoesNotExist


def populate_phenotype_map(apps, schema_editor):
    Recipe = apps.get_model('genetics_manager', 'CommercialPhenotypeRecipe')
    Trait = apps.get_model('calculator', 'Trait')
    Allele = apps.get_model('calculator', 'Allele')
    GenotypePhenotype = apps.get_model('calculator', 'GenotypePhenotype')

    with transaction.atomic():
        for recipe_obj in Recipe.objects.all():
            if not recipe_obj.phenotype or not recipe_obj.required_genotypes:
                continue

            # Iterate over the JSON data: {'Locus Name': 'Allele1/Allele2'}
            for trait_name, genotype_string in recipe_obj.required_genotypes.items():
                alleles = genotype_string.split('/')
                if len(alleles) != 2: continue
                al1_name, al2_name = alleles

                # Fetch the actual DB objects for the alleles and trait
                try:
                    trait_obj = Trait.objects.get(name=trait_name)
                    allele1_obj = Allele.objects.get(trait=trait_obj, name=al1_name)
                    allele2_obj = Allele.objects.get(trait=trait_obj, name=al2_name)

                except ObjectDoesNotExist:
                    print(f"Missing data for mapping: {trait_name} ({genotype_string})")
                    continue

                # Create the GenotypePhenotype mapping (handles A/B and B/A automatically due to unique_together constraint)
                # We use the recipe_obj.phenotype as the result string
                GenotypePhenotype.objects.get_or_create(
                    trait=trait_obj,
                    allele1=allele1_obj,
                    allele2=allele2_obj,
                    defaults={'phenotype': recipe_obj.phenotype}
                )


def reverse_populate_phenotype_map(apps, schema_editor):
    # Deletes all GenotypePhenotype records created by this migration
    GenotypePhenotype = apps.get_model('calculator', 'GenotypePhenotype')
    # Warning: this deletes ALL records in the table. If you have manual data, this will remove it.
    GenotypePhenotype.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        # Depends on the previous migration where we seeded Traits and Alleles
        ('calculator', '0007_seed_and_populate_genotypes'),
        ('genetics_manager', '0009_alter_commercialphenotyperecipe_breeder_name'),
    ]

    operations = [
        migrations.RunPython(populate_phenotype_map, reverse_populate_phenotype_map),
    ]
