import fish  # ensure fish.py is importable
from cbr.models import CommercialPhenotypeRecipe

ALLELE_TO_LOCUS = {
    "L": "Lightning",
    "O": "Onyx",
    "a": "Albino",
    "G": "Goldflake",
    "WB": "Widebar",
    "N": "Naked",
    "DV": "DaVinci",
    "P": "Picasso",
    "Sf": "Snowflake",
}


def parse_genotype(genotype_str):
    genotype_str = genotype_str.strip()
    if genotype_str == "+/+":
        return [("Wild", ("+", "+"))]

    allele_pairs = genotype_str.split()
    types = []
    for pair in allele_pairs:
        alleles = pair.split("/")
        locus_name = ALLELE_TO_LOCUS.get(alleles[0], "Unknown")
        types.append((locus_name, tuple(alleles)))
    return types


parents = CommercialPhenotypeRecipe.objects.all()
results = []

for parent1 in parents:
    f1_types = parse_genotype(parent1.genotype)
    f1 = fish.fish(f1_types)

    for parent2 in parents:
        f2_types = parse_genotype(parent2.genotype)
        f2 = fish.fish(f2_types)

        results = fish.cross_fish(f1, f2)

        # for key in results.keys():
        #     if str(key) == '':
        #         print ('+/+: ' + str(results[key]),
        #         parent1.name, parent2.name)
        #     else:
        #         print (str(key) + ': ' +
        #         str(results[key]), parent1.name, parent2.name)

        for genotype_str in results.keys():
            # print((lambda g: g if g.strip() else '+/+')
            # (genotype_str), parent1.name, parent2.name)

            phenotype_name = fish.pheno(genotype_str, parent1.name, parent2.name)
            result = {
                "cross_parents": f"{parent1.name} x {parent2.name}",
                "genotype": (lambda g: g if g.strip() else "+/+")(genotype_str),
                "phenotype_name": phenotype_name.replace("(", "").replace(")", ""),
            }
            if "X" not in phenotype_name:
                print(result)
            # results.append(result)
        #     # Print each result so you see output immediately
        #     print(json.dumps(result))
