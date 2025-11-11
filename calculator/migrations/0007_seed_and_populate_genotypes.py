# calculator/migrations/0007_seed_and_populate_genotypes.py (Corrected)

from django.db import migrations, transaction
from django.core.exceptions import ObjectDoesNotExist


def seed_and_associate_clownfish_genotypes(apps, schema_editor):
    # Get models from the apps registry (historical versions)
    Locus = apps.get_model('genetics_manager', 'Locus')
    Recipe = apps.get_model('genetics_manager', 'CommercialPhenotypeRecipe')
    Clownfish = apps.get_model('calculator', 'Clownfish')
    ClownfishGenotype = apps.get_model('calculator', 'ClownfishGenotype')
    Trait = apps.get_model('calculator', 'Trait')
    Allele = apps.get_model('calculator', 'Allele')

    # 1. SEEDING PHASE: Populate Trait and Allele tables from Locus model

    with transaction.atomic():
        for locus_obj in Locus.objects.all():
            # Create Trait (uses get_or_create to be safe)
            trait_obj, created = Trait.objects.get_or_create(
                name=locus_obj.name,
                # REMOVED: defaults={'description': locus_obj.help_text}
            )

            # Create Alleles for this trait using the ArrayField data
            for allele_name in locus_obj.alleles:
                Allele.objects.get_or_create(
                    trait=trait_obj,
                    name=allele_name,
                    defaults={'display_name': allele_name}
                )

    # ... (the rest of the function remains the same) ...
    # 2. ASSOCIATION PHASE: ...

    # Helper function to find an allele object safely (now guaranteed to exist)
    def get_allele_object(trait_name, allele_name):
        try:
            trait_obj = Trait.objects.get(name=trait_name)
            return Allele.objects.get(trait=trait_obj, name=allele_name)
        except ObjectDoesNotExist:
            print(f"CRITICAL ERROR: Missing Trait/Allele post-seeding: {trait_name} / {allele_name}")
            return None

    with transaction.atomic():
        for recipe_obj in Recipe.objects.all():
            if not recipe_obj.required_genotypes:
                continue

            try:
                clownfish_obj = Clownfish.objects.get(name=recipe_obj.name)
            except Clownfish.DoesNotExist:
                continue

            for trait_name, genotype_string in recipe_obj.required_genotypes.items():
                alleles = genotype_string.split('/')
                if len(alleles) != 2: continue
                allele1_name, allele2_name = alleles

                al1 = get_allele_object(trait_name, allele1_name)
                al2 = get_allele_object(trait_name, allele2_name)

                if al1 and al2:
                    trait_obj = Trait.objects.get(name=trait_name)
                    ClownfishGenotype.objects.get_or_create(
                        clownfish=clownfish_obj,
                        trait=trait_obj,
                        defaults={
                            'allele1': al1,
                            'allele2': al2,
                        }
                    )


def reverse_seed_and_associate(apps, schema_editor):
    ClownfishGenotype = apps.get_model('calculator', 'ClownfishGenotype')
    Allele = apps.get_model('calculator', 'Allele')
    Trait = apps.get_model('calculator', 'Trait')

    ClownfishGenotype.objects.all().delete()
    Allele.objects.all().delete()
    Trait.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ('calculator', '0006_clownfish_hybrid_clownfish_variant'),
        ('genetics_manager', '0009_alter_commercialphenotyperecipe_breeder_name'),
    ]

    operations = [
        migrations.RunPython(seed_and_associate_clownfish_genotypes, reverse_seed_and_associate),
    ]

