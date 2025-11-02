import re

file_path = "phenotype.py"
output_path = "cleaned_phenotype.py"

# Read the entire content of the file
try:
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
except FileNotFoundError:
    print(f"Error: The file '{file_path}' was not found.")
    exit()

# Define a single pattern to capture both conditions
# The pattern finds a colon, followed by any amount of whitespace (including newlines),
# and then the word "pheno".
pattern = r":\s+(pheno)"

# Replace the matched pattern with a colon, a single space, and the captured "pheno"
cleaned_content = re.sub(pattern, r": \1", content)

# Write the modified content to the SAME file (overwriting it each time)
# The 'w' mode ensures the file is overwritten on each run
with open(output_path, "w", encoding="utf-8") as file:
    file.write(cleaned_content)

print(f"File cleaned and saved to {output_path}")
