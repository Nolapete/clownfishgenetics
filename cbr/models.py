from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import JSONField, Q


class Variety(models.Model):
    """Represents a named clownfish variety, e.g., 'Picasso'."""

    name = models.CharField(max_length=100, unique=True)
    genus = models.CharField(max_length=100)
    species = models.CharField(max_length=100)
    variant = models.CharField(max_length=255, blank=True)
    hybrid = models.BooleanField(default=False)
    genotype_pattern = models.CharField(max_length=50)

    class Meta:
        verbose_name_plural = "Varieties"

    def __str__(self):
        return f"{self.name} {self.genotype_pattern}"


class Parent(models.Model):
    """Represents a specific fish used for breeding."""

    variety = models.ForeignKey(Variety, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Parents"

    def __str__(self):
        return str(self.variety)


class Cross(models.Model):
    """Represents a breeding cross between two parents."""

    parent1 = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="crosses_as_parent1"
    )
    parent2 = models.ForeignKey(
        Parent, on_delete=models.CASCADE, related_name="crosses_as_parent2"
    )

    class Meta:
        verbose_name_plural = "Crosses"

    def __str__(self):
        return f"{self.parent1} X {self.parent2}"


class Progeny(models.Model):
    """Represents an offspring from a specific cross."""

    cross = models.ForeignKey(Cross, on_delete=models.CASCADE)
    genotype = models.CharField(max_length=50)
    phenotype_name = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name_plural = "Progeny"  # The plural of progeny is also progeny.

    # MOVED: __str__ is now before save()
    def __str__(self):
        return f"{self.phenotype_name} ({self.genotype})"

    def save(self, *args, **kwargs):
        from .services import get_progeny_phenotype_name

        # Generate the phenotype name if it's not already set
        if not self.phenotype_name:
            self.phenotype_name = get_progeny_phenotype_name(self.cross, self.genotype)
        super().save(*args, **kwargs)


class CrossNamingRule(models.Model):
    """Represents a specific named cross between two varieties."""

    variety1 = models.ForeignKey(
        Variety, on_delete=models.CASCADE, related_name="naming_rules_as_variety1"
    )
    variety2 = models.ForeignKey(
        Variety, on_delete=models.CASCADE, related_name="naming_rules_as_variety2"
    )

    class Meta:
        # Enforce a unique combination regardless of order
        unique_together = ("variety1", "variety2")
        verbose_name_plural = "Cross Naming Rules"

    def __str__(self):
        return f"Rule for {self.variety1} X {self.variety2}"


class ProgenyNamingRule(models.Model):
    """Stores the specific phenotype name for a genotype from a named cross."""

    cross_rule = models.ForeignKey(CrossNamingRule, on_delete=models.CASCADE)
    genotype_pattern = models.CharField(max_length=50)
    phenotype_name = models.CharField(max_length=150)

    class Meta:
        # A single genotype pattern should be unique per cross rule
        unique_together = ("cross_rule", "genotype_pattern")
        verbose_name_plural = "Progeny Naming Rules"

    def __str__(self):
        return f"{self.phenotype_name} ({self.genotype_pattern})"


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
    """
    Represents a commercial phenotype recipe for clownfish genetics,
    including required genotypes, phenotype info, and legacy data fields.
    """

    objects = models.Manager()

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The commercial brand name, e.g., 'Black Ice'",
    )
    breeder_name = models.CharField(max_length=100, blank=True)
    required_genotypes = models.JSONField(
        blank=True,
        default=dict,
        help_text=(
            "JSON dictionary mapping Locus name to required genotype. "
            "Format: {'Locus Name': 'Allele1/Allele2'}"
        ),
    )
    description = models.TextField(blank=True)

    # Fields for legacy data from animals.json
    phenotype = models.CharField(max_length=255, unique=True, blank=True)
    slug = models.SlugField(blank=True)
    genotype = models.CharField(max_length=255, blank=True, default="+/+")
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

    @property
    def is_pure_wild_type(self):
        return all(gene_pair == "+/+" for gene_pair in self.genotype.split())

    def criteria(self, result_dict):
        if not self.required_genotypes or self.required_genotypes == {}:
            return all(val == "+/+" for val in result_dict.values())
        for locus, required_gt in self.required_genotypes.items():
            if result_dict.get(locus) != required_gt:
                return False
        return True
