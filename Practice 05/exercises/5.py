import re

# Match a string that has 'a', anything, then 'b'

text = input("Enter text: ")

matches = re.findall(r"a.*b", text)

print(matches)