import sqlite3
import matplotlib.pyplot as plt
from venn import venn

# Database path
DB_PATH = "../db/textrank_unique.db"

# Category mapping
CATEGORY_MAPPING = {"A": "cordis", "B": "crunchbase", "C": "wipo", "D": "wos"}

# Connect to database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Fetch all unique words for each category
category_words = {}

for key, category in CATEGORY_MAPPING.items():
    cursor.execute(
        f"SELECT DISTINCT keyword FROM keywords WHERE origin = ?", (category,)
    )
    category_words[key] = {row[0] for row in cursor.fetchall()}

conn.close()

# Print category sizes
for key, words in category_words.items():
    print(f"Loaded {len(words)} unique words for {CATEGORY_MAPPING[key]} ({key})")

# Compute intersections
ABCD = len(
    category_words["A"]
    & category_words["B"]
    & category_words["C"]
    & category_words["D"]
)
ABC = len(category_words["A"] & category_words["B"] & category_words["C"]) - ABCD
ABD = len(category_words["A"] & category_words["B"] & category_words["D"]) - ABCD
ACD = len(category_words["A"] & category_words["C"] & category_words["D"]) - ABCD
BCD = len(category_words["B"] & category_words["C"] & category_words["D"]) - ABCD

AB = len(category_words["A"] & category_words["B"]) - (ABC + ABD + ABCD)
AC = len(category_words["A"] & category_words["C"]) - (ABC + ACD + ABCD)
AD = len(category_words["A"] & category_words["D"]) - (ABD + ACD + ABCD)
BC = len(category_words["B"] & category_words["C"]) - (ABC + BCD + ABCD)
BD = len(category_words["B"] & category_words["D"]) - (ABD + BCD + ABCD)
CD = len(category_words["C"] & category_words["D"]) - (ACD + BCD + ABCD)

A_only = len(category_words["A"]) - (AB + AC + AD + ABC + ABD + ACD + ABCD)
B_only = len(category_words["B"]) - (AB + BC + BD + ABC + ABD + BCD + ABCD)
C_only = len(category_words["C"]) - (AC + BC + CD + ABC + ACD + BCD + ABCD)
D_only = len(category_words["D"]) - (AD + BD + CD + ABD + ACD + BCD + ABCD)

# Venn data structure
venn_data = {
    "1000": A_only,
    "0100": B_only,
    "0010": C_only,
    "0001": D_only,
    "1100": AB,
    "1010": AC,
    "1001": AD,
    "0110": BC,
    "0101": BD,
    "0011": CD,
    "1110": ABC,
    "1101": ABD,
    "1011": ACD,
    "0111": BCD,
    "1111": ABCD,
}

print("\nComputed Venn regions:")
for region, count in venn_data.items():
    print(f"{region}: {count}")

# Create sets for the Venn diagram
sets_dict = {key: set() for key in CATEGORY_MAPPING.keys()}
dummy_elements = {}
counter = 0

for region, count in venn_data.items():
    dummy_elements[region] = [f"{region}_{i}" for i in range(counter, counter + count)]
    counter += count

# Assign elements to appropriate sets
for region, elems in dummy_elements.items():
    if region[0] == "1":
        sets_dict["A"].update(elems)
    if region[1] == "1":
        sets_dict["B"].update(elems)
    if region[2] == "1":
        sets_dict["C"].update(elems)
    if region[3] == "1":
        sets_dict["D"].update(elems)

# Print final category sizes
print("\nSet sizes (should match computed totals):")
for key, s in sets_dict.items():
    print(f"{key}: {len(s)}")

# Generate Venn diagram with actual category names
plt.figure(figsize=(20, 20))  # Increase figure size
venn({CATEGORY_MAPPING[key]: value for key, value in sets_dict.items()})
# plt.title("4-Set Venn Diagram")
plt.tight_layout()  # Reduce whitespace
plt.show()
