import re

# Task 2
# Match a string that has an 'a' followed by two to three 'b'
# Regex: ab{2,3}
# Explanation:
# a       -> the letter 'a'
# b{2,3}  -> the letter 'b' repeated from 2 to 3 times

# Ask the user to input text
text = input("Enter text: ")
#ab abb a abbbb ac

# Find all matches where 'a' is followed by 2 or 3 'b'
matches = re.findall(r"ab{2,3}", text)
print(matches) 