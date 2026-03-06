import re

# Task 6
# Replace all spaces, commas, and dots with a colon (:)

# Regex explanation:
# [ ,.]  -> square brackets mean "any one of these characters"
# space  -> matches a space
# ,      -> matches a comma
# .      -> matches a dot

# Ask the user to enter text
text = input("Enter text: ")

# re.sub(pattern, replacement, text)
# pattern -> what we want to find
# replacement -> what we replace it with
# text -> the original string

result = re.sub(r"[ ,.]", ":", text)

# Print the modified text
print(result)