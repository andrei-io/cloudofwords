import matplotlib.pyplot as plt
from venn import venn

# --------------------------
# Your provided counts
# --------------------------
# Totals for each set
A_total = 1654
B_total = 2622
C_total = 2549
D_total = 21788

# Given pair intersections (these include all deeper intersections):
AB = 671
AC = 532
AD = 1380
BC = 627
BD = 1817
CD = 1878

# Given triple intersections:
ABC = 349
ABD = 660
ACD = 530
BCD = 620

# Given quadruple intersection:
ABCD = 348

# Calculate the exact counts for triple-only regions:
ABC_only = ABC - ABCD  # 349 - 348 = 1
ABD_only = ABD - ABCD  # 660 - 348 = 312
ACD_only = ACD - ABCD  # 530 - 348 = 182
BCD_only = BCD - ABCD  # 620 - 348 = 272

# Calculate the pair-only regions.
AB_only = AB - (ABC_only + ABD_only + ABCD)  # 671 - (1 + 312 + 348) = 10
AC_only = AC - (ABC_only + ACD_only + ABCD)  # 532 - (1 + 182 + 348) = 1
AD_only = AD - (ABD_only + ACD_only + ABCD)  # 1380 - (312 + 182 + 348) = 538
BC_only = BC - (ABC_only + BCD_only + ABCD)  # 627 - (1 + 272 + 348) = 6
BD_only = BD - (ABD_only + BCD_only + ABCD)  # 1817 - (312 + 272 + 348) = 885
CD_only = CD - (ACD_only + BCD_only + ABCD)  # 1878 - (182 + 272 + 348) = 1076

# Compute the "only" regions for the individual sets.
A_only = A_total - (AB_only + AC_only + AD_only + ABC_only + ABD_only + ACD_only + ABCD)
B_only = B_total - (AB_only + BC_only + BD_only + ABC_only + ABD_only + BCD_only + ABCD)
C_only = C_total - (AC_only + BC_only + CD_only + ABC_only + ACD_only + BCD_only + ABCD)
D_only = D_total - (AD_only + BD_only + CD_only + ABD_only + ACD_only + BCD_only + ABCD)

# Create a dictionary for the 15 regions.
# The keys are 4-digit binary strings indicating membership in [A, B, C, D].
venn_data = {
    "1000": A_only,  # Only A
    "0100": B_only,  # Only B
    "0010": C_only,  # Only C
    "0001": D_only,  # Only D
    "1100": AB_only,  # A and B only
    "1010": AC_only,  # A and C only
    "1001": AD_only,  # A and D only
    "0110": BC_only,  # B and C only
    "0101": BD_only,  # B and D only
    "0011": CD_only,  # C and D only
    "1110": ABC_only,  # A, B, and C only
    "1101": ABD_only,  # A, B, and D only
    "1011": ACD_only,  # A, C, and D only
    "0111": BCD_only,  # B, C, and D only
    "1111": ABCD,  # A, B, C, and D
}

print("Computed Venn regions:")
for region, count in venn_data.items():
    print(f"{region}: {count}")

# --------------------------
# Build dummy sets from the counts
# --------------------------
# For each region, we generate a list of dummy element names.
# We'll then add these elements to the appropriate sets.
dummy_elements = {}
counter = 0
for region, count in venn_data.items():
    # Create a unique dummy element name for each item in the region.
    dummy_elements[region] = [f"{region}_{i}" for i in range(counter, counter + count)]
    counter += count

# Now build the sets A, B, C, and D.
# The region key is a 4-character string: position 0 for A, 1 for B, etc.
sets_dict = {"A": set(), "B": set(), "C": set(), "D": set()}

for region, elems in dummy_elements.items():
    if region[0] == "1":  # belongs to A
        sets_dict["A"].update(elems)
    if region[1] == "1":  # belongs to B
        sets_dict["B"].update(elems)
    if region[2] == "1":  # belongs to C
        sets_dict["C"].update(elems)
    if region[3] == "1":  # belongs to D
        sets_dict["D"].update(elems)

# Verify that the computed set sizes match your provided totals.
print("\nSet sizes (should match provided totals):")
for key, s in sets_dict.items():
    print(f"{key}: {len(s)}")

# --------------------------
# Generate and display the Venn diagram
# --------------------------
venn(sets_dict)
plt.title("4-Set Venn Diagram")
plt.show()
