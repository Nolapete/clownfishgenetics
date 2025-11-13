from django.contrib import admin

from .models import CommercialPhenotypeRecipe, Locus


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
