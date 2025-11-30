# In clownfishgenetics/cbr/calculator_utils.py
# No Django model imports!


class fish:
    """A holder for the traits and genotypes of a fish, as a dictionary."""

    def __init__(self, types_dict):
        self.types = types_dict

    def get_types(self):
        return self.types


def format_allele(p1, p2):
    """'/' = wildtype allele, output +/+ format for Progeny matching"""
    # Map '/' → '+' for Progeny DB matching
    a1 = "+" if p1 == "/" else p1
    a2 = "+" if p2 == "/" else p2

    # Dominant first
    if a1 != "+" and a2 != "+" and ord(a1[0]) < ord(a2[0]):
        return f"{a1}/{a2}"
    return f"{a2}/{a1}" if a2 != "+" else f"{a1}/+" if a1 != "+" else "+/+"


def cross_at_index(ind, length, h_axis, v_axis):
    x, y = ind
    geno_parts = []

    for ax_ind in range(len(h_axis)):
        x_bit_set = (x >> ax_ind) & 1
        y_bit_set = (y >> ax_ind) & 1
        xpart = h_axis[ax_ind][1 - x_bit_set]
        ypart = v_axis[ax_ind][1 - y_bit_set]

        geno = format_allele(xpart, ypart)  # ← FIXED! G/+ not +/G
        geno_parts.append(geno)

    non_wild = [g for g in geno_parts if g != "+/+"]
    return " ".join(non_wild) if non_wild else "+/+"


def cross_fish_structured(f1, f2):
    """v11: Safe indexing fixed"""
    VALID_LOCI = ["Sf", "N", "P", "DV", "L", "O", "WB", "G", "a"]

    LOCI_MAP = {
        "Snowflake": "Sf",
        "Naked": "N",
        "Albino": "a",
        "Picasso": "P",
        "DaVinci": "DV",
        "Lightning": "L",
        "Onyx": "O",
        "Widebar": "WB",
        "Goldflake": "G",
    }

    LOCUS_ORDER = {loci: i for i, loci in enumerate(VALID_LOCI)}

    f1_types = f1.get_types().copy()
    f2_types = f2.get_types().copy()

    def parse_and_map(trait_dict):
        parsed = {}
        for trait_name, geno in trait_dict.items():
            locus = LOCI_MAP.get(trait_name, trait_name)
            if locus in VALID_LOCI and isinstance(geno, str) and "/" in geno:
                alleles = geno.split("/")
                parsed[locus] = (alleles[0], alleles[1])
            else:
                parsed[locus] = ("/", "/")
        return parsed

    f1_types = parse_and_map(f1_types)
    f2_types = parse_and_map(f2_types)

    valid_traits = [
        locus for locus in VALID_LOCI if locus in f1_types or locus in f2_types
    ]
    all_trait_names = sorted(valid_traits, key=lambda x: LOCUS_ORDER[x])

    f1_final = [f1_types.get(name, ("/", "/")) for name in all_trait_names]
    f2_final = [f2_types.get(name, ("/", "/")) for name in all_trait_names]

    print(f"MAPPED TRAITS: {all_trait_names}")
    print(f"ALIGNED f1_final: {f1_final}")
    print(f"ALIGNED f2_final: {f2_final}")

    table_length = 2 ** len(f1_final)
    results_list = []

    for x in range(table_length):
        for y in range(table_length):
            genotype_str = cross_at_index((x, y), table_length, f1_final, f2_final)
            genotype_list = genotype_str.split()

            # ✅ SAFE INDEXING
            non_wild = []
            for i in range(len(all_trait_names)):
                geno = genotype_list[i] if i < len(genotype_list) else "+/+"
                if geno != "+/+":
                    non_wild.append(geno)
            # progeny_key = ' '.join(non_wild) if non_wild else "+/+"
            progeny_key = genotype_str

            # ✅ SAFE DICT
            genotype_dict = {}
            for i, name in enumerate(all_trait_names):
                geno = genotype_list[i] if i < len(genotype_list) else "+/+"
                genotype_dict[name] = geno
            genotype_dict["PROGENY_KEY"] = progeny_key

            results_list.append(genotype_dict)

    return results_list, table_length**2, all_trait_names


def analyze_results_by_recipe(results_list, total_count, recipes, all_trait_names):
    """Counts the occurrences of each phenotype recipe in the results list."""
    phenotype_counts = {}

    for result_dict in results_list:
        matched = False
        for recipe in recipes:
            if recipe["criteria"](result_dict):
                name = recipe["name"]
                phenotype_counts[name] = phenotype_counts.get(name, 0.0) + (
                    100.0 / total_count
                )
                matched = True
                break  # Still first-match-wins, but now criteria must be precise

        # Optional: Handle unmatched (add default recipe last)
        if not matched:
            phenotype_counts["Unmatched"] = phenotype_counts.get("Unmatched", 0.0) + (
                100.0 / total_count
            )

    return phenotype_counts
