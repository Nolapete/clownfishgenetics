# clownfishgenetics/calcRefactor/models.py

from django.db import models


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
        return f'{self.species} "{self.name}"'


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
