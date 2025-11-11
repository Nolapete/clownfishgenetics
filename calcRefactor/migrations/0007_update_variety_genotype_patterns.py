# clownfishgenetics/calcRefactor/migrations/0007_update_variety_genotype_patterns.py

from django.db import migrations, transaction


def update_genotype_patterns(apps, schema_editor):
    Recipe = apps.get_model('genetics_manager', 'CommercialPhenotypeRecipe')
    Variety = apps.get_model('calcRefactor', 'Variety')

    with transaction.atomic():
        for recipe_obj in Recipe.objects.all():
            # Find the corresponding Variety object that was created in the last migration
            try:
                # Use get() as name is unique in both models
                variety_obj = Variety.objects.get(name=recipe_obj.name)
            except Variety.DoesNotExist:
                continue  # Skip if no matching variety found

            # --- Logic to use the 'genotype' char field data ---
            if recipe_obj.genotype:
                # Assuming the format is a pipe-separated string like 'A/a|B/b'
                # We can just copy it directly, or clean it up if needed.
                variety_obj.genotype_pattern = recipe_obj.genotype
            else:
                variety_obj.genotype_pattern = "No specific pattern defined"

            variety_obj.save()


def reverse_update_genotype_patterns(apps, schema_editor):
    # Optional: Logic to clear the field on rollback
    Variety = apps.get_model('calcRefactor', 'Variety')
    Variety.objects.all().update(genotype_pattern="N/A")


class Migration(migrations.Migration):
    dependencies = [
        ('calcRefactor', '0006_auto_20251111_2133'),
        ('genetics_manager', '0009_alter_commercialphenotyperecipe_breeder_name'),
    ]

    operations = [
        migrations.RunPython(update_genotype_patterns, reverse_update_genotype_patterns),
    ]
