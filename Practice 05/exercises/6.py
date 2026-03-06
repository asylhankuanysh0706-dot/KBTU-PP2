import re

# Task 6
# Replace all occurrences of space, comma, or dot with a colon

# Regex explanation:
# [ ,.]
# [ ]   -> character set
# space -> matches a space
# ,     -> matches a comma
# .     -> matches a dot
# Any of these characters will be replaced with ':'

# Ask the user to enter text

text = input("Enter text: ")#Hello, world. Python regex

# Replace space, comma, or dot with ':'
result = re.sub(r"[ ,.]", ":", text)

print(result)