from django.contrib import admin

from .models import Cross, CrossNamingRule, Parent, Progeny, ProgenyNamingRule, Variety


# A TabularInline for ProgenyNamingRule makes it easy to add rules
# directly on the CrossNamingRule admin page.
class ProgenyNamingRuleInline(admin.TabularInline):
    model = ProgenyNamingRule
    extra = 1


@admin.register(CrossNamingRule)
class CrossNamingRuleAdmin(admin.ModelAdmin):
    list_display = ("variety1", "variety2")
    inlines = [ProgenyNamingRuleInline]


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ("name", "species", "genotype_pattern")
    search_fields = ("name", "species")


@admin.register(Parent)
class ParentAdmin(admin.ModelAdmin):
    list_display = ("id", "variety")
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
