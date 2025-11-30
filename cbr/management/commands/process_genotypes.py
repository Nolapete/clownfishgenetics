# In clownfishgenetics/genetics_manager/management/commands/process_genotypes.py


from django.core.management.base import BaseCommand

from genetics_manager.models import CommercialPhenotypeRecipe, Locus


class Command(BaseCommand):
    help = (
        'Parses the raw "genotype" string field into the structured '
        '"required_genotypes" JSON field.'
    )

    def handle(self, *args, **options):
        self.stdout.write("Starting genotype processing...")

        # --- BUILD THE LOCUS MAP DYNAMICALLY FROM THE DATABASE ---
        # Initialize an empty map
        locus_names_map = {}
        # Iterate over all Locus records
        for locus in Locus.objects.all():
            # For each allele in the locus's alleles list, map it back to the locus name
            # e.g., locus.alleles = ['P', 'Sf'], locus.name = 'Overbar'
            # We map 'P' -> 'Overbar' and 'Sf' -> 'Overbar'
            for allele in locus.alleles:
                locus_names_map[allele] = locus.name
        # --------------------------------------------------------

        recipes = CommercialPhenotypeRecipe.objects.all()
        count = 0

        for recipe in recipes:
            # 1. Ensure the name field is populated correctly
            # first from the phenotype data
            if not recipe.name and recipe.phenotype:
                recipe.name = recipe.phenotype.strip()

            raw_genotype_string = recipe.genotype
            if not raw_genotype_string or recipe.required_genotypes:
                continue

            structured_genotypes = {}
            gene_pairs = raw_genotype_string.split()

            for pair in gene_pairs:
                allele1, allele2 = pair.split("/")

                locus_name = None
                if allele1 != "+":
                    locus_name = locus_names_map.get(allele1)
                elif allele2 != "+":
                    locus_name = locus_names_map.get(allele2)

                if locus_name:
                    structured_genotypes[locus_name] = pair
                else:
                    if pair != "+/+":
                        self.stdout.write(
                            self.style.WARNING(
                                f"Unknown locus/allele: {pair} in recipe ID {recipe.pk}"
                            )
                        )

            recipe.required_genotypes = structured_genotypes
            recipe.save()
            count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully processed {count} recipes.")
        )
