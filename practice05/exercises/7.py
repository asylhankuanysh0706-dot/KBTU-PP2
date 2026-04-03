import re

# Task 7
# Convert snake_case string to camelCase

# Regex: _([a-z])
# Explanation:
# _        -> matches the underscore
# ([a-z])  -> captures the lowercase letter after the underscore
# lambda m -> takes the captured letter and converts it to uppercase

# Ask the user to enter a snake_case string
text = input("Enter snake_case: ")#hello_world


# Replace "_letter" with the uppercase version of the letter
result = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), text)

print(result)