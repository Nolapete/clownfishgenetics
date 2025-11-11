from django.contrib.postgres.fields import ArrayField
from django.db import models


class Locus(models.Model):
    name = models.CharField(
        max_length=50, unique=True, help_text="e.g., Overbar, Onyx, Lightning"
    )
    alleles = ArrayField(
        models.CharField(max_length=5),
        default=list,
        help_text="e.g., ['P', 'Sf', 'O', '+', 'L', 'N']",
    )

    class Meta:
        verbose_name_plural = "Loci"

    def __str__(self):
        return self.name


class CommercialPhenotypeRecipe(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The commercial brand name, e.g., 'Black Ice'",
    )
    breeder_name = models.CharField(max_length=100, blank=True)
    required_genotypes = models.JSONField(
        blank=True,
        help_text="JSON dictionary mapping Locus name to required "
        "genotype. Format: {'Locus Name': 'Allele1/Allele2'}",
    )
    description = models.TextField(blank=True)

    # Fields for legacy data from animals.json
    phenotype = models.CharField(max_length=255, unique=True, blank=True)
    slug = models.SlugField(blank=True)
    genotype = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=50, blank=True)
    species = models.CharField(max_length=50, blank=True)
    variant = models.CharField(max_length=255, blank=True)
    hybrid = models.BooleanField(default=False)
    date_added = models.DateTimeField(null=True, blank=True)
    origin = models.CharField(max_length=50, blank=True)
    created_by = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Phenotype Recipe"
        verbose_name_plural = "Phenotype Recipes"

    def __str__(self):
        return self.name
