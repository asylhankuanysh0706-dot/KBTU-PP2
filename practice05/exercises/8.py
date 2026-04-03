import re

# Task 8
# Split a string at uppercase letters

# Regex: (?=[A-Z])
# Explanation:
# (?= )  -> positive lookahead (checks the next character without removing it)
# [A-Z]  -> any uppercase letter
# The string will be split right before every uppercase letter

# Ask the user to enter a camelCase or PascalCase string
text = input("Enter text: ")#MyVariableName

# Split the string at positions before uppercase letters

result = re.split(r"(?=[A-Z])", text)

print(result)