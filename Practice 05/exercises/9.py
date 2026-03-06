import re
# Task 9
# Insert spaces between words starting with capital letters

# Regex: ([A-Z])
# Explanation:
# ([A-Z]) -> finds every uppercase letter
# r" \1"  -> inserts a space before that letter
# \1      -> refers to the matched uppercase letter
# .strip() -> removes a space if it appears at the beginning

# Ask the user to input a camelCase or PascalCase string
text = input("Enter text: ")#HelloWorldPython

# Insert spaces before uppercase letters

result = re.sub(r"([A-Z])", r" \1", text).strip()

print(result)