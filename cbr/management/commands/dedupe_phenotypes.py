# In your project: genetics_manager/management/commands/dedupe_phenotypes.py

from django.core.management.base import BaseCommand
from django.db import models, transaction

from genetics_manager.models import CommercialPhenotypeRecipe


class Command(BaseCommand):
    help = (
        "Deduplicates records, prioritizing those with non-+/+"
        " genotypes or longer descriptions."
    )

    def handle(self, *args, **options):
        self.stdout.write(
            "Starting robust deduplication of CommercialPhenotypeRecipe records..."
        )

        duplicates = (
            CommercialPhenotypeRecipe.objects.values("phenotype")
            .order_by()
            .annotate(count_id=models.Count("id"))
            .filter(count_id__gt=1)
        )

        deleted_count = 0

        for duplicate in duplicates:
            phenotype_name = duplicate["phenotype"]

            # Get all records for this specific phenotype name,
            # sorted by ID to ensure consistency
            all_records = list(
                CommercialPhenotypeRecipe.objects.filter(
                    phenotype=phenotype_name
                ).order_by("id")
            )

            record_to_keep = None

            # Priority A: Check if any record has a genotype that is NOT +/+
            for record in all_records:
                if record.genotype != "+/+":
                    record_to_keep = record
                    break  # Found the winner based on the specific criteria

            # Priority B: If NO winner was found in A (meaning ALL records were +/+),
            # we use the length as a tie-breaker.
            if record_to_keep is None:
                record_to_keep = max(all_records, key=lambda x: len(x.phenotype))
                # Note: If lengths are identical, it keeps the first one
                # in the list (arbitrary but consistent)

            # 4. Delete all records *except* the chosen one within a transaction
            with transaction.atomic():
                records_to_delete = CommercialPhenotypeRecipe.objects.filter(
                    phenotype=phenotype_name
                ).exclude(id=record_to_keep.id)
                count_deleted, _ = records_to_delete.delete()
                deleted_count += count_deleted

                self.stdout.write(
                    self.style.WARNING(
                        f"Deleted {count_deleted} duplicate(s) for '{phenotype_name}' "
                        f"(Kept ID {record_to_keep.id}, "
                        f"Genotype: {record_to_keep.genotype})"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Deduplication complete. Total records deleted: {deleted_count}"
            )
        )
