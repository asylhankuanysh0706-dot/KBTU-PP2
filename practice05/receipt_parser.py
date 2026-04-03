import re
import json

path = r"C:\Users\Quanysh\Desktop\KBTU-PP2\Practice 05\raw.txt"

with open(path, encoding="utf-8") as f:
    text = f.read()

products_data = re.findall(r"^\d+\.\s+(.+)\n[\s\S]*?([\d ]+,\d{2})(?=\nСтоимость| \d+,\d{2} x|\n\d+\.)", text, re.MULTILINE)

names = []
prices_str = []
prices_float = []

for item in products_data:
    name = item[0].strip()
    price_raw = item[1].replace(" ", "").replace(",", ".")
    
    names.append(name)
    prices_str.append(item[1].strip())
    prices_float.append(float(price_raw))

total = sum(prices_float)


date_match = re.search(r"\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}", text)


pay_match = re.search(r"Способ оплаты:\s*(.+)|(Банковская карта|Наличные)", text, re.IGNORECASE)
pay_method = pay_match.group().strip() if pay_match else "Не указан"

data = {
    "products": names,
    "prices": prices_str,
    "total_amount": round(total, 2),
    "date": date_match.group() if date_match else None,
    "payment_method": pay_method
}

print(json.dumps(data, indent=4, ensure_ascii=False))
