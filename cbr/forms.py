from django import forms

from .models import Clownfish, Cross, Parent, Variety


class VarietyForm(forms.ModelForm):
    class Meta:
        model = Variety
        fields = ["name", "species", "genotype_pattern"]


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ["variety"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Improve the display of the Variety dropdown
        self.fields["variety"].queryset = Variety.objects.order_by("species", "name")


class CrossForm(forms.ModelForm):
    class Meta:
        model = Cross
        fields = ["parent1", "parent2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: Improve the display of the Parent dropdowns
        self.fields["parent1"].queryset = Parent.objects.select_related(
            "variety"
        ).order_by("variety__species", "variety__name")
        self.fields["parent2"].queryset = Parent.objects.select_related(
            "variety"
        ).order_by("variety__species", "variety__name")


# Form for a single-gene (monohybrid) cross
class GenotypeForm(forms.Form):
    """Form to select the genotypes for a monohybrid cross."""

    GENOTYPE_CHOICES = [
        ("PP", "Picasso (PP)"),
        ("Pp", "Misbar (Pp)"),
        ("pp", "Regular (pp)"),
    ]
    parent1_genotype = forms.ChoiceField(
        label="Parent 1 Genotype (Color)", choices=GENOTYPE_CHOICES
    )
    parent2_genotype = forms.ChoiceField(
        label="Parent 2 Genotype (Color)", choices=GENOTYPE_CHOICES
    )


# Form for a two-gene (dihybrid) cross
class DihybridForm(forms.Form):
    """Form to select genotypes for a dihybrid cross involving two independent genes."""

    # Gene 1: Coloration
    COLOR_GENOTYPE_CHOICES = [
        ("PP", "Picasso (PP)"),
        ("Pp", "Misbar (Pp)"),
        ("pp", "Regular (pp)"),
    ]
    parent1_color_genotype = forms.ChoiceField(
        label="Parent 1 Color Genotype", choices=COLOR_GENOTYPE_CHOICES
    )
    parent2_color_genotype = forms.ChoiceField(
        label="Parent 2 Color Genotype", choices=COLOR_GENOTYPE_CHOICES
    )

    # Gene 2: Stripe Pattern
    STRIPE_GENOTYPE_CHOICES = [
        ("SS", "Solid Stripe (SS)"),
        ("Ss", "Broken Stripe (Ss)"),
        ("ss", "Absent Stripe (ss)"),
    ]
    parent1_stripe_genotype = forms.ChoiceField(
        label="Parent 1 Stripe Genotype", choices=STRIPE_GENOTYPE_CHOICES
    )
    parent2_stripe_genotype = forms.ChoiceField(
        label="Parent 2 Stripe Genotype", choices=STRIPE_GENOTYPE_CHOICES
    )


# Form for a single gene with multiple alleles
class MultipleAlleleForm(forms.Form):
    """Form to select genotypes for a gene with multiple alleles (e.g., R1, R2, R3)."""

    # Assuming R1 > R2 > R3 dominance hierarchy for this example
    ALLELE_CHOICES = [
        ("R1R1", "R1R1"),
        ("R1R2", "R1R2"),
        ("R1R3", "R1R3"),
        ("R2R2", "R2R2"),
        ("R2R3", "R2R3"),
        ("R3R3", "R3R3"),
    ]
    parent1_genotype = forms.ChoiceField(
        label="Parent 1 Genotype", choices=ALLELE_CHOICES
    )
    parent2_genotype = forms.ChoiceField(
        label="Parent 2 Genotype", choices=ALLELE_CHOICES
    )


class ParentSelectionForm(forms.Form):
    """
    Form for selecting parent clownfish from existing records.
    """

    parent1 = forms.ModelChoiceField(
        queryset=Clownfish.objects.all(),
        label="Parent 1",
        empty_label="Select a clownfish",
    )
    parent2 = forms.ModelChoiceField(
        queryset=Clownfish.objects.all(),
        label="Parent 2",
        empty_label="Select a clownfish",
    )
