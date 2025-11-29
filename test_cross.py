# test_cross.py - Standalone genetics tester
from genetics_manager.calculator_utils import cross_at_index_fixed


def test_sf_n_cross():
    """Exact replica of your Sf x N cross"""
    # Mock your parsed f1_final/f2_final from debug
    f1_final = [("/", "/"), ("Sf", "+")]  # Snowflake parent
    f2_final = [("N", "+"), ("/", "/")]  # Chocolate Midnight parent
    all_trait_names = ["N", "Snowflake"]  # From your ALIGNED debug

    print("=== STANDALONE SF/N CROSS TEST ===")
    table_length = 2 ** len(f1_final)  # 4
    results = []

    for x in range(table_length):
        for y in range(table_length):
            geno_str = cross_at_index_fixed((x, y), table_length, f1_final, f2_final)
            geno_list = geno_str.split()
            geno_dict = {
                all_trait_names[i]: geno_list[i] for i in range(len(geno_list))
            }
            results.append(geno_dict)
            print(f"({x},{y}): {geno_str} → {geno_dict}")

    progeny_map = {
        "+/+": "Chocolate Mocha",
        "N/+": "Chocolate Midnight",
        "Sf/+": "Blacker Ice",
        "N/+ Sf/+": "Blacker Lightning",
    }

    print("\n=== RESULTS vs PROGENY ===")
    for r in results:
        geno_key = " ".join(r.values())
        print(f"'{geno_key}' → {progeny_map.get(geno_key, '❌ MISSING')}")


if __name__ == "__main__":
    test_sf_n_cross()
