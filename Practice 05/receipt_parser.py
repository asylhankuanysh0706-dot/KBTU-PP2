import re
import json
with open("raw.txt") as f:
    txt=f.read()


# 1. Extract all prices from receipt
# Regex explanation:
# Стоимость        -> literal word "Стоимость" (used in receipt)
# \s*\n           -> optional spaces then newline
# ([\d ]+,\d{2})  -> capture number format like "1 234,56"
#                     [\d ]+ means digits with possible spaces
#                     ,\d{2} means comma and two decimals

num = re.findall(r"Стоимость\s*\n([\d ]+,\d{2})", txt)

# Convert extracted price strings to float numbers
cl_p=[]
for p in num:# Steps:
# 1. Remove spaces
# 2. Replace comma with dot
# 3. Convert the string to float
   clean = p.replace(" ", "").replace(",", ".")
   cl_p.append(float(clean))
total=sum(cl_p)


# Extract product names
# Regex explanation:
# ^\d+\.  -> product number like "1."
# \s*\n   -> spaces followed by newline
# (.+)    -> captures the product name
#
# re.MULTILINE allows ^ to match the start of each line
name = re.findall(r"^\d+\.\s*\n(.+)", txt, re.MULTILINE)
date=re.search(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}",txt )# Extract date and time
Pay_m=re.search(r"Банковская карта|Наличные", txt)# Extract payment method
# Create structured JSON output
data = {
    "products": name,           # list of product names
    "price": num,               # extracted price strings
    "total amount": total,      # calculated total price
    "date": date.group(),       # extracted date and time
    "Pay method": Pay_m.group() # payment method
}

print(json.dumps(data, indent=4, ensure_ascii=False))