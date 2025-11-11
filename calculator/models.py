from django.db import models
from django.db.models import JSONField, Q


class UserGenotype(models.Model):
    """
    A model to store a user's defined genotype for calculation.
    Uses a ManyToManyField to link traits, and a JSONField to hold the allele pair.
    """

    name = models.CharField(max_length=100)
    alleles = JSONField(
        default=dict
    )  # Stores allele pairs like {'Color': ['PP'], 'Stripe': ['Ss']}

    def __str__(self):
        return self.name


class Trait(models.Model):
    """
    Represents a genetic trait, e.g., 'Color' or 'Stripe Pattern'.
    """

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    INHERITANCE_CHOICES = [
        ("dominant", "Dominant/Recessive"),
        ("codominant", "Codominant"),
        ("incomplete", "Incomplete Dominance"),
    ]
    inheritance_pattern = models.CharField(
        max_length=20, choices=INHERITANCE_CHOICES, default="dominant"
    )

    def __str__(self):
        return self.name


class Allele(models.Model):
    """
    Represents a specific allele for a trait, e.g., 'R' for 'Red' color.
    """

    trait = models.ForeignKey(Trait, on_delete=models.CASCADE, related_name="alleles")
    name = models.CharField(max_length=50)  # e.g., 'R', 'W'
    display_name = models.CharField(max_length=100)  # e.g., 'Red' or 'White'

    def __str__(self):
        return f"{self.trait.name}: {self.display_name} ({self.name})"


class GenotypePhenotype(models.Model):
    """
    Maps a specific genotype (allele pair) to a resulting phenotype.
    """

    trait = models.ForeignKey(
        Trait, on_delete=models.CASCADE, related_name="phenotypes"
    )
    allele1 = models.ForeignKey(Allele, on_delete=models.CASCADE, related_name="+")
    allele2 = models.ForeignKey(Allele, on_delete=models.CASCADE, related_name="+")
    phenotype = models.CharField(max_length=200)

    class Meta:
        unique_together = ("trait", "allele1", "allele2")
        indexes = [
            models.Index(fields=["trait", "allele1", "allele2"]),
        ]

    def __str__(self):
        return f"{self.get_genotype_string()} -> {self.phenotype}"

    def get_genotype_string(self):
        alleles = sorted([self.allele1.name, self.allele2.name])
        return "".join(alleles)


class Clownfish(models.Model):
    """
    Represents an individual clownfish with its species and genetic information.
    """

    name = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    variant = models.CharField(max_length=255, blank=True)
    hybrid = models.BooleanField(default=False)
    # Specify the through_fields to resolve the ambiguity
    genotype = models.ManyToManyField(
        Allele,
        through="ClownfishGenotype",
        through_fields=(
            "clownfish",
            "allele1",
        ),  # Use the clownfish and first allele for the relation
    )

    class Meta:
        verbose_name_plural = "Clownfish"

    def __str__(self):
        return f"{self.name} ({self.genus} {self.species})"

    def get_phenotype_string(self):
        """Generates a descriptive phenotype string for the clownfish."""
        phenotype_parts = [
            genotype.get_phenotype() for genotype in self.clownfishgenotype_set.all()
        ]
        return ", ".join(phenotype_parts)

    def get_trait_genotype(self, trait_name):
        """Returns the allele names for a specific trait."""
        alleles = [
            g.allele.name
            for g in self.clownfishgenotype_set.filter(trait__name=trait_name)
        ]
        return alleles

    @property
    def full_species_name(self):
        return f"{self.genus} {self.species}"


class ClownfishGenotype(models.Model):
    clownfish = models.ForeignKey(Clownfish, on_delete=models.CASCADE)
    trait = models.ForeignKey(Trait, on_delete=models.CASCADE)
    allele1 = models.ForeignKey(
        Allele, on_delete=models.CASCADE, related_name="allele1_set"
    )
    allele2 = models.ForeignKey(
        Allele, on_delete=models.CASCADE, related_name="allele2_set"
    )

    class Meta:
        unique_together = ("clownfish", "trait")

    def __str__(self):
        return self.clownfish

    def get_phenotype(self):
        try:
            alleles = sorted([self.allele1.name, self.allele2.name])

            # The Q object needs to be combined with the trait argument.
            # Q objects are passed as *args and combined using the `&` operator.
            q_lookup = Q(trait=self.trait) & (
                Q(allele1__name=alleles[0], allele2__name=alleles[1])
                | Q(allele1__name=alleles[1], allele2__name=alleles[0])
            )

            # Now, you can pass the single combined Q object as the positional argument.
            phenotype_map = GenotypePhenotype.objects.get(q_lookup)

            return f"{self.trait.name}: {phenotype_map.phenotype}"
        except GenotypePhenotype.DoesNotExist:
            return f"{self.trait.name}: Unknown (No mapping found)"
        except GenotypePhenotype.MultipleObjectsReturned:
            # This case is less likely with the corrected Q object, but is good practice
            return f"{self.trait.name}: Error (Multiple mappings found)"
