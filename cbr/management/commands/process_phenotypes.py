import json
import os
import re

from django.core.management.base import BaseCommand, CommandError

from genetics_manager.models import CommercialPhenotypeRecipe


class Command(BaseCommand):
    help = (
        "Generates a JSON fixture file (phenotype_recipes.json) from an "
        "input list, skipping existing DB records."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "input_filename",
            type=str,
            help="The input text file containing phenotype names (one per line).",
        )

    def handle(self, *args, **options):
        input_file = options["input_filename"]

        if not os.path.isfile(input_file):
            raise CommandError(f"File not found at the specified path: {input_file}")

        names_list = []
        try:
            with open(input_file, encoding="utf-8") as f:
                for line in f:
                    stripped_line = line.strip()
                    if stripped_line and not stripped_line.startswith("#"):
                        if stripped_line.startswith("- "):
                            clean_name = stripped_line[2:].strip()
                        else:
                            clean_name = stripped_line
                        if clean_name:
                            names_list.append(clean_name)
        except FileNotFoundError as err:
            raise CommandError(f"Error: '{input_file}' was not found.") from err

        data = []
        skipped_count = 0

        name_pattern = re.compile(
            r"^(?P<genus>\w+)\s*(?P<species_part>.*?)\s*" r"(?P<variant>\"[^\"]+\")?$"
        )

        for full_name in names_list:
            if CommercialPhenotypeRecipe.objects.filter(phenotype=full_name).exists():
                self.stdout.write(
                    self.style.WARNING(f"Skipping existing record in DB: {full_name}")
                )
                skipped_count += 1
                continue

            name = full_name.replace("*", "").strip()
            genus, species, variant, is_hybrid = "", "", "", False

            match = name_pattern.match(name)
            if match:
                parts = match.groupdict()
                genus = (parts.get("genus") or "").strip()
                middle = (parts.get("species_part") or "").strip()
                variant = (parts.get("variant") or "").strip()
                if variant and middle:
                    species = middle.strip()
                    if genus == "Pramphiprion":
                        is_hybrid = True
                elif genus and variant and not middle:
                    is_hybrid = True
                    species = ""
                elif middle and not variant:
                    species = middle.strip()

            entry = {
                "model": "genetics_manager.commercialphenotyperecipe",
                "fields": {
                    "name": full_name,
                    "phenotype": full_name,
                    "slug": "",
                    "genotype": "+/+",
                    "genus": genus,
                    "species": species,
                    "variant": variant,
                    "hybrid": is_hybrid,
                    "origin": "clownfish",
                    "created_by": 1,
                    "required_genotypes": {},
                },
            }
            data.append(entry)

        output_file = "phenotype_recipes.json"
        with open(output_file, "w") as f:
            f.write(json.dumps(data, indent=2))

        self.stdout.write(
            self.style.SUCCESS(
                f"Processing complete. Generated file with {len(data)} "
                f"NEW entries, skipped {skipped_count} existing ones."
            )
        )
