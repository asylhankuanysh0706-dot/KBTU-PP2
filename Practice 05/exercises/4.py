import re

# Task 4
# Find sequences of one uppercase letter followed by lowercase letters

# Regex: [A-Z][a-z]+
# Explanation:
# [A-Z]  -> one uppercase letter
# [a-z]+ -> one or more lowercase letters

# Ask the user for input

text = input("Enter text: ")
#Apple banana Cat dog Elephant

# Find all words that start with a capital letter followed by lowercase letters
matches = re.findall(r"[A-Z][a-z]+", text)

print(matches)