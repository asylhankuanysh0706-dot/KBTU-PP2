import re

# Task 3
# Find sequences of lowercase letters joined with an underscore

# Regex: [a-z]+_[a-z]+
# Explanation:
# [a-z]+  -> one or more lowercase letters
# _       -> underscore
# [a-z]+  -> again one or more lowercase letters

# Ask user for input

text =input("Enter text:")
#hello_world test_var abc_def

# Find all snake_case style words
matches = re.findall(r"[a-z]+_[a-z]+", text)
print(matches)