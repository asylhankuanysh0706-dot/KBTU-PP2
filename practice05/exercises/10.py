import re

# Task 10
# Convert a given camelCase string to snake_case

# Regex: ([A-Z])
# Explanation:
# ([A-Z]) -> finds every uppercase letter
# r"_\1"  -> adds an underscore before the uppercase letter
# \1      -> refers to the matched uppercase letter
# .lower() -> converts the whole string to lowercase

# Ask the user to input a camelCase string
text = input("Enter camelCase: ")

# Insert '_' before every uppercase letter and convert to lowercase
result = re.sub(r"([A-Z])", r"_\1", text).lower()

print(result)