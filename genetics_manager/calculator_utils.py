# In clownfishgenetics/genetics_manager/calculator_utils.py
# No Django model imports!


class fish:
    """A holder for the traits and genotypes of a fish, as a dictionary."""

    def __init__(self, types_dict):
        self.types = types_dict

    def get_types(self):
        return self.types


def format_allele(p1, p2):
    """Ensures dominant (uppercase/non-wild) allele comes first
    in the display string."""
    if p1 == "+":
        if "a" <= p2 <= "z":
            return p1 + "/" + p2
        return p2 + "/" + p1
    elif p2 == "+":
        if "a" <= p1 <= "z":
            return p2 + "/" + p1
    return p1 + "/" + p2


def cross_at_index(ind, length, h_axis, v_axis):
    """Calculates the genotype at a specific index in the
    virtual Punnett square table."""
    start = length // 2
    x, y = ind
    res_parts = []
    ax_ind = 0

    while start > 0:
        xpart = h_axis[ax_ind] if x >= start else h_axis[ax_ind]
        ypart = v_axis[ax_ind] if y >= start else v_axis[ax_ind]
        if xpart != "+" or ypart != "+":
            res_parts.append(format_allele(xpart, ypart))

        x %= start
        y %= start
        start //= 2
        ax_ind += 1

    return " ".join(res_parts)


def cross_fish_structured(f1, f2):
    """Performs a cross and returns a structured list of genotype dictionaries."""
    f1_types = f1.get_types().copy()
    f2_types = f2.get_types().copy()
    f1_type_names = set(f1_types.keys())
    f2_type_names = set(f2_types.keys())

    for n in f2_type_names - f1_type_names:
        f1_types[n] = ("+", "+")
    for n in f1_type_names - f2_type_names:
        f2_types[n] = ("+", "+")

    all_trait_names = sorted(f1_type_names.union(f2_type_names))
    f1_final = [f1_types[name] for name in all_trait_names]
    f2_final = [f2_types[name] for name in all_trait_names]

    table_length = 2 ** len(f1_final)
    results_list = []

    for x in range(table_length):
        for y in range(table_length):
            genotype_list = cross_at_index(
                (x, y), table_length, f1_final, f2_final
            ).split()
            genotype_dict = {}

            for i, name in enumerate(all_trait_names):
                if i < len(genotype_list):
                    genotype_dict[name] = genotype_list[i]
                else:
                    genotype_dict[name] = "+/+"

            results_list.append(genotype_dict)

    return results_list, table_length**2, all_trait_names


def analyze_results_by_recipe(results_list, total_count, recipes, all_trait_names):
    """Counts the occurrences of each phenotype recipe in the results list."""
    phenotype_counts = {}

    for result_dict in results_list:
        for recipe in recipes:
            if recipe["criteria"](result_dict):
                name = recipe["name"]
                phenotype_counts[name] = phenotype_counts.get(name, 0.0) + (
                    100.0 / total_count
                )
                break

    return phenotype_counts
