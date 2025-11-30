from django.contrib import admin

from .models import (
    Allele,
    Clownfish,
    ClownfishGenotype,
    CommercialPhenotypeRecipe,
    Cross,
    CrossNamingRule,
    GenotypePhenotype,
    Locus,
    Parent,
    Progeny,
    ProgenyNamingRule,
    Trait,
    UserGenotype,
    Variety,
)


# A TabularInline for ProgenyNamingRule makes it easy to add rules
# directly on the CrossNamingRule admin page.
class ProgenyNamingRuleInline(admin.TabularInline):
    model = ProgenyNamingRule
    extra = 1


@admin.register(CrossNamingRule)
class CrossNamingRuleAdmin(admin.ModelAdmin):
    list_display = ("variety1", "variety2")
    autocomplete_fields = ("variety1", "variety2")
    inlines = [ProgenyNamingRuleInline]


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "genotype_pattern")
    search_fields = ("name", "species")


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("variety",)
    list_filter = ("variety",)
    search_fields = ("variety__name",)


@admin.register(Cross)
class CrossAdmin(admin.ModelAdmin):
    list_display = ("parent1", "parent2")
    list_filter = ("parent1__variety", "parent2__variety")


@admin.register(Progeny)
class ProgenyAdmin(admin.ModelAdmin):
    list_display = ("cross", "genotype", "phenotype_name")
    list_filter = ("cross", "phenotype_name")
    search_fields = ("genotype", "phenotype_name")
    readonly_fields = ("phenotype_name",)  # Ensure this is not manually edited


@admin.register(UserGenotype)
class UserGenotypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


# Inline for editing ClownfishGenotype records directly on the Clownfish page
class ClownfishGenotypeInline(admin.TabularInline):
    model = ClownfishGenotype
    extra = 1
    # Use raw_id_fields for Alleles to make it easier to select many options
    raw_id_fields = ["allele1", "allele2"]


# ModelAdmin for the Clownfish model
@admin.register(Clownfish)
class ClownfishAdmin(admin.ModelAdmin):
    list_display = ("name", "genus", "species", "get_phenotype_string")
    inlines = [ClownfishGenotypeInline]

    # Optional: Display the phenotype string in the list view
    def get_phenotype_string(self, obj):
        return obj.get_phenotype_string()

    get_phenotype_string.short_description = "Phenotype"


# Inline for editing Allele records directly on the Trait page
class AlleleInline(admin.TabularInline):
    model = Allele
    extra = 1


# Inline for editing GenotypePhenotype records directly on the Trait page
class GenotypePhenotypeInline(admin.TabularInline):
    model = GenotypePhenotype
    extra = 1
    fk_name = "trait"
    raw_id_fields = ["allele1", "allele2"]


# ModelAdmin for the Trait model
@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ("name", "inheritance_pattern")
    inlines = [AlleleInline, GenotypePhenotypeInline]


# Register Allele and GenotypePhenotype as standard models as well,
# in case you need to manage them independently.
@admin.register(Allele)
class AlleleAdmin(admin.ModelAdmin):
    list_display = ("name", "display_name", "trait")
    list_filter = ("trait",)


@admin.register(GenotypePhenotype)
class GenotypePhenotypeAdmin(admin.ModelAdmin):
    list_display = ("get_genotype_string", "phenotype", "trait")
    list_filter = ("trait",)

    def get_genotype_string(self, obj):
        return obj.get_genotype_string()

    get_genotype_string.short_description = "Genotype"


class LocusAdmin(admin.ModelAdmin):
    list_display = ("name", "display_alleles")
    search_fields = ("name",)

    def display_alleles(self, obj):
        return ", ".join(obj.alleles)

    display_alleles.short_description = "Alleles"


class CommercialPhenotypeRecipeAdmin(admin.ModelAdmin):
    list_display = ("name", "genotype", "variant", "hybrid", "display_genotype_json")
    search_fields = ("name", "genotype", "variant")
    list_filter = ("hybrid", "genus", "species")

    def display_genotype_json(self, obj):
        return str(obj.required_genotypes)

    display_genotype_json.short_description = "Req. Genotypes (JSON)"


admin.site.register(Locus, LocusAdmin)
admin.site.register(CommercialPhenotypeRecipe, CommercialPhenotypeRecipeAdmin)
