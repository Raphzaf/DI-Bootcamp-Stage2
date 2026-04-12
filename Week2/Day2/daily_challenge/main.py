MATRIX_STR = '''
7ir
Tsi
h%x
i ?
sM# 
$a 
#t%'''

# Step 1: Convert matrix_string to a 2D list (matrix)
matrix = [list(row) for row in MATRIX_STR.strip().split('\n')]

# Step 2: Collect all characters column by column (top to bottom, left to right)
num_cols = max(len(row) for row in matrix)

all_chars = []
for col in range(num_cols):
    for row in matrix:
        if col < len(row):
            all_chars.append(row[col])

# Steps 3 & 4: Filter alpha characters and replace non-alpha gaps with a single space
decoded_message = ""
in_alpha_section = False
has_gap = False

for char in all_chars:
    if char.isalpha():
        # Add a space only if there was a non-alpha gap between two alpha groups
        if has_gap and in_alpha_section:
            decoded_message += " "
        decoded_message += char
        in_alpha_section = True
        has_gap = False
    else:
        if in_alpha_section:
            has_gap = True

# Step 5: Print the decoded message
print(decoded_message)
