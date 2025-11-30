from django.db import migrations


def forwards(apps, schema_editor):
    # Old models from respective apps
    OldVariety = apps.get_model("calcRefactor", "Variety")
    OldParent = apps.get_model("calcRefactor", "Parent")
    OldCross = apps.get_model("calcRefactor", "Cross")
    OldProgeny = apps.get_model("calcRefactor", "Progeny")

    OldLocus = apps.get_model("genetics_manager", "Locus")
    OldRecipe = apps.get_model("genetics_manager", "CommercialPhenotypeRecipe")

    OldTrait = apps.get_model("calculator", "Trait")
    OldAllele = apps.get_model("calculator", "Allele")
    OldGenotypePhenotype = apps.get_model("calculator", "GenotypePhenotype")
    OldClownfish = apps.get_model("calculator", "Clownfish")
    OldClownfishGenotype = apps.get_model("calculator", "ClownfishGenotype")

    # New models in cbr app
    NewVariety = apps.get_model("cbr", "Variety")
    NewParent = apps.get_model("cbr", "Parent")
    NewCross = apps.get_model("cbr", "Cross")
    NewProgeny = apps.get_model("cbr", "Progeny")

    NewLocus = apps.get_model("cbr", "Locus")
    NewRecipe = apps.get_model("cbr", "CommercialPhenotypeRecipe")

    NewTrait = apps.get_model("cbr", "Trait")
    NewAllele = apps.get_model("cbr", "Allele")
    NewGenotypePhenotype = apps.get_model("cbr", "GenotypePhenotype")
    NewClownfish = apps.get_model("cbr", "Clownfish")
    NewClownfishGenotype = apps.get_model("cbr", "ClownfishGenotype")

    # Copy Locus data
    for old in OldLocus.objects.all():
        NewLocus.objects.update_or_create(
            pk=old.pk,
            defaults={
                "name": old.name,
                "alleles": old.alleles,
            },
        )

    # Copy CommercialPhenotypeRecipe data
    for old in OldRecipe.objects.all():
        NewRecipe.objects.update_or_create(
            pk=old.pk,
            defaults={
                "name": old.name,
                "breeder_name": old.breeder_name,
                "required_genotypes": old.required_genotypes,
                "description": old.description,
                "phenotype": old.phenotype,
                "slug": old.slug,
                "genotype": old.genotype,
                "genus": old.genus,
                "species": old.species,
                "variant": old.variant,
                "hybrid": old.hybrid,
                "date_added": old.date_added,
                "origin": old.origin,
                "created_by": old.created_by,
            },
        )

    # Copy Traits
    for trait in OldTrait.objects.all():
        NewTrait.objects.update_or_create(
            pk=trait.pk,
            defaults={
                "name": trait.name,
                "description": trait.description,
                "inheritance_pattern": trait.inheritance_pattern,
            },
        )

    # Copy Alleles
    for allele in OldAllele.objects.all():
        NewAllele.objects.update_or_create(
            pk=allele.pk,
            defaults={
                "trait_id": allele.trait_id,
                "name": allele.name,
                "display_name": allele.display_name,
            },
        )

    # Copy GenotypePhenotype
    for gp in OldGenotypePhenotype.objects.all():
        NewGenotypePhenotype.objects.update_or_create(
            pk=gp.pk,
            defaults={
                "trait_id": gp.trait_id,
                "allele1_id": gp.allele1_id,
                "allele2_id": gp.allele2_id,
                "phenotype": gp.phenotype,
            },
        )

    # Copy Varieties
    for old in OldVariety.objects.all():
        NewVariety.objects.update_or_create(
            pk=old.pk,
            defaults={
                "name": old.name,
                "genus": old.genus,
                "species": old.species,
                "variant": old.variant,
                "hybrid": old.hybrid,
                "genotype_pattern": old.genotype_pattern,
            },
        )

    # Copy Parents
    for old in OldParent.objects.all():
        NewParent.objects.update_or_create(
            pk=old.pk,
            defaults={
                "variety_id": old.variety_id,
            },
        )

    # Copy Crosses
    for old in OldCross.objects.all():
        NewCross.objects.update_or_create(
            pk=old.pk,
            defaults={
                "parent1_id": old.parent1_id,
                "parent2_id": old.parent2_id,
            },
        )

    # Copy Progeny
    for old in OldProgeny.objects.all():
        NewProgeny.objects.update_or_create(
            pk=old.pk,
            defaults={
                "cross_id": old.cross_id,
                "genotype": old.genotype,
                "phenotype_name": old.phenotype_name,
            },
        )

    # Copy Clownfish
    for old in OldClownfish.objects.all():
        NewClownfish.objects.update_or_create(
            pk=old.pk,
            defaults={
                "name": old.name,
                "genus": old.genus,
                "species": old.species,
                "variant": old.variant,
                "hybrid": old.hybrid,
            },
        )

    # Copy ClownfishGenotype
    for old in OldClownfishGenotype.objects.all():
        NewClownfishGenotype.objects.update_or_create(
            pk=old.pk,
            defaults={
                "clownfish_id": old.clownfish_id,
                "trait_id": old.trait_id,
                "allele1_id": old.allele1_id,
                "allele2_id": old.allele2_id,
            },
        )


def backwards(apps, schema_editor):
    # Optional: implement rollback logic if needed
    pass


class Migration(migrations.Migration):
    dependencies = [
        ("cbr", "0001_initial"),
        ("calcRefactor", "0007_update_variety_genotype_patterns"),
        ("genetics_manager", "0012_alter_commercialphenotyperecipe_required_genotypes"),
        ("calculator", "0008_populate_genotype_phenotype_map"),
    ]

    operations = [
        migrations.RunPython(forwards, backwards),
    ]
