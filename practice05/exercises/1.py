import re

# Task 1
# Match a string that has an 'a' followed by zero or more 'b'
# Regex: ab*
# Explanation:
# a  -> the letter 'a'
# b* -> zero or more 'b'

# Ask user for input


text = input("Enter text:")
#ab abb a abbbb ac

# Find all matches of pattern 'a' followed by 0 or more 'b'
matches = re.findall(r"ab*", text)
print(matches)