from django.contrib import admin
from .models import Trait, Allele, UserGenotype, GenotypePhenotype
from .models import Clownfish, ClownfishGenotype

@admin.register(UserGenotype)
class UserGenotypeAdmin(admin.ModelAdmin):
    list_display = ('name',) 

# Inline for editing ClownfishGenotype records directly on the Clownfish page
class ClownfishGenotypeInline(admin.TabularInline):
    model = ClownfishGenotype
    extra = 1
    # Use raw_id_fields for Alleles to make it easier to select many options
    raw_id_fields = ['allele1', 'allele2']

# ModelAdmin for the Clownfish model
@admin.register(Clownfish)
class ClownfishAdmin(admin.ModelAdmin):
    list_display = ('name', 'genus', 'species', 'get_phenotype_string')
    inlines = [ClownfishGenotypeInline]
    
    # Optional: Display the phenotype string in the list view
    def get_phenotype_string(self, obj):
        return obj.get_phenotype_string()
    get_phenotype_string.short_description = 'Phenotype'

# Inline for editing Allele records directly on the Trait page
class AlleleInline(admin.TabularInline):
    model = Allele
    extra = 1

# Inline for editing GenotypePhenotype records directly on the Trait page
class GenotypePhenotypeInline(admin.TabularInline):
    model = GenotypePhenotype
    extra = 1
    fk_name = 'trait'
    raw_id_fields = ['allele1', 'allele2']

# ModelAdmin for the Trait model
@admin.register(Trait)
class TraitAdmin(admin.ModelAdmin):
    list_display = ('name', 'inheritance_pattern')
    inlines = [AlleleInline, GenotypePhenotypeInline]

# Register Allele and GenotypePhenotype as standard models as well,
# in case you need to manage them independently.
@admin.register(Allele)
class AlleleAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_name', 'trait')
    list_filter = ('trait',)

@admin.register(GenotypePhenotype)
class GenotypePhenotypeAdmin(admin.ModelAdmin):
    list_display = ('get_genotype_string', 'phenotype', 'trait')
    list_filter = ('trait',)
    
    def get_genotype_string(self, obj):
        return obj.get_genotype_string()
    get_genotype_string.short_description = 'Genotype'

